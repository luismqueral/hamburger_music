from string import ascii_lowercase
import random
import xml.etree.ElementTree as ET
import html
from string import ascii_letters
import re

import requests

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_GET_CAPTION_URL = "https://www.youtube.com/api/timedtext"


class NoSuitableText(Exception):
    pass


#####################Original author: tzot, in a response at StackOverflow######################################
import unicodedata as ud

latin_letters = {}


def is_latin(uchr):
    try:
        return latin_letters[uchr]
    except KeyError:
        return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))


def only_roman_chars(unistr):
    return all(is_latin(uchr)
               for uchr in unistr
               if uchr.isalpha())


################################################################################################################

def capitalize(text):
    return text[0].upper() + text[1:]


class Poet(object):
    nothing = [None, '', ' ']

    @staticmethod
    def stripbeginnonletters(text):
        while not (text[0] in ascii_letters) and len(text) > 1:
            text = text[1:]
        return text

    def __init__(self, key, wordrange, capitalize, whitelist, blacklist, randomness=2, languages=None,
                 lines_per_video=2, minsublength=3):
        if not languages:
            languages = ['en']
        self.key = key
        self.wordrange = wordrange
        self.capitalize = capitalize
        self.whitelist = whitelist
        self.blacklist = blacklist
        self.randomness = randomness
        self.languages = languages
        self.lines_per_video = lines_per_video
        self.minsublength = minsublength
        self.genLine = self.lineGenerator()

    def isnothing(self, item):
        return item in Poet.nothing or len(item) < self.minsublength

    def getVideo(self):
        randomstr = ''.join([random.choice(ascii_lowercase) for i in range(self.randomness)])
        parameters = {"key": self.key,
                      "part": "id",
                      "maxResults": 50,
                      "order": "date",
                      "q": randomstr,
                      "type": "video",
                      "videoCaption": "closedCaption",
                      "fields": "items/id/videoId"}
        results = requests.get(YOUTUBE_SEARCH_URL, parameters).json()
        id = random.choice(results['items'])['id']['videoId']
        return id

    def getLang(self, id):
        parameters = {"v": id,
                      "expire": 1,
                      "type": "list"}
        results = requests.get(YOUTUBE_GET_CAPTION_URL, parameters).text
        try:
            tree = ET.fromstring(results)
        except ET.ParseError:
            raise NoSuitableText
        languages = [{'lang_code': track.attrib['lang_code'], 'name': track.attrib['lang_original']} for track in
                     tree.findall('track')]
        for language in languages:
            if language['lang_code'] in self.languages:
                return language
        raise NoSuitableText

    def getLines(self, id, lang):
        parameters = {"v": id,
                      "lang": lang['lang_code']}
        results = requests.get(YOUTUBE_GET_CAPTION_URL, parameters).text
        try:
            tree = ET.fromstring(results)
        except ET.ParseError:
            raise NoSuitableText
        alllines = [capitalize(html.unescape(Poet.stripbeginnonletters(line.text.replace('\n', '')))) for line
                    in tree.findall('text') if
                    not self.isnothing(line.text) and only_roman_chars(str(line.text)) and len(
                        line.text.split()) in self.wordrange]
        alllines = self.filterBlacklist(self.filterWhitelist(alllines))

        if len(alllines) == 0:
            raise NoSuitableText
        elif len(alllines) < self.lines_per_video:
            lines = alllines
        else:
            lines = random.sample(alllines, self.lines_per_video)
        return lines

    def lineGenerator(self):
        linecache = []
        while True:
            if len(linecache) > 0:
                yield linecache.pop(0)
            else:
                try:
                    id = self.getVideo()
                    lang = self.getLang(id)
                    lines = self.getLines(id, lang)
                except NoSuitableText:
                    continue
                linecache.extend(lines[1:])
                yield lines[0]

    def filterWhitelist(self, lines):
        return [line for line in lines if
                not self.whitelist or any([line.__contains__(whitelistentry) for whitelistentry in self.whitelist])]

    def filterBlacklist(self, lines):
        return [line for line in lines if
                not any([line.__contains__(blacklistentry) for blacklistentry in self.blacklist])]

    def makePoem(self, number_of_lines):
        poemlist = [next(self.genLine) for i in range(number_of_lines)]
        random.shuffle(poemlist)
        poem = '\n'.join(poemlist)
        return strip_html(poem)


def strip_html(text):
    return re.sub('<[^<]+?>', '', text)
