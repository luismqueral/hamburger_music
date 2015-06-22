#  __    __   ______   __       __  _______   __    __  _______    ______   ________  _______  
# /  |  /  | /      \ /  \     /  |/       \ /  |  /  |/       \  /      \ /        |/       \ 
# $$ |  $$ |/$$$$$$  |$$  \   /$$ |$$$$$$$  |$$ |  $$ |$$$$$$$  |/$$$$$$  |$$$$$$$$/ $$$$$$$  |
# $$ |__$$ |$$ |__$$ |$$$  \ /$$$ |$$ |__$$ |$$ |  $$ |$$ |__$$ |$$ | _$$/ $$ |__    $$ |__$$ |
# $$    $$ |$$    $$ |$$$$  /$$$$ |$$    $$< $$ |  $$ |$$    $$< $$ |/    |$$    |   $$    $$< 
# $$$$$$$$ |$$$$$$$$ |$$ $$ $$/$$ |$$$$$$$  |$$ |  $$ |$$$$$$$  |$$ |$$$$ |$$$$$/    $$$$$$$  |
# $$ |  $$ |$$ |  $$ |$$ |$$$/ $$ |$$ |__$$ |$$ \__$$ |$$ |  $$ |$$ \__$$ |$$ |_____ $$ |  $$ |
# $$ |  $$ |$$ |  $$ |$$ | $/  $$ |$$    $$/ $$    $$/ $$ |  $$ |$$    $$/ $$       |$$ |  $$ |
# $$/   $$/ $$/   $$/ $$/      $$/ $$$$$$$/   $$$$$$/  $$/   $$/  $$$$$$/  $$$$$$$$/ $$/   $$/ 
                                                                                                                                                                                        
#  __       __  __    __   ______   ______   ______                                            
# /  \     /  |/  |  /  | /      \ /      | /      \                                           
# $$  \   /$$ |$$ |  $$ |/$$$$$$  |$$$$$$/ /$$$$$$  |                                          
# $$$  \ /$$$ |$$ |  $$ |$$ \__$$/   $$ |  $$ |  $$/                                           
# $$$$  /$$$$ |$$ |  $$ |$$      \   $$ |  $$ |                                                
# $$ $$ $$/$$ |$$ |  $$ | $$$$$$  |  $$ |  $$ |   __                                           
# $$ |$$$/ $$ |$$ \__$$ |/  \__$$ | _$$ |_ $$ \__/  |                                          
# $$ | $/  $$ |$$    $$/ $$    $$/ / $$   |$$    $$/                                           
# $$/      $$/  $$$$$$/   $$$$$$/  $$$$$$/  $$$$$$/                                            
                                                                                             

# designed by luis queral (www.luisquer.al)
# engineered by elon bing
# found live at www.hamburgermusic.tumblr.com
# 2014



####################################################

from sys import exit

try:
    from settings import *
except ImportError:
    exit("Error, no settings-file found. Create a settings.py file, or edit and rename samplesettings.py to settings.py")
    

import json
from urllib import urlopen
from string import ascii_lowercase
import random
import xml.etree.ElementTree as ET
from HTMLParser import HTMLParser
from string import ascii_letters
import re

class NoSuitableText(Exception):
    pass

#####################Original author: tzot, in a response at StackOverflow######################################
import unicodedata as ud
latin_letters= {}
def is_latin(uchr):
    try: return latin_letters[uchr]
    except KeyError:
        return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))

def only_roman_chars(unistr):
    return all(is_latin(uchr)
           for uchr in unistr
           if uchr.isalpha())
################################################################################################################

def capitalize(text):
    return text[0].upper()+text[1:]

class Poet(object):
    nothing=[None,'',' ']
    @staticmethod
    def isnothing(item):
        return item in Poet.nothing or len(item)<MINSUBLENGTH
    
    @staticmethod
    def stripbeginnonletters(text):
        while not (text[0] in ascii_letters) and len(text)>1:
            text=text[1:]
        return text

    def __init__(self,key,wordrange,capitalize,whitelist,blacklist,randomness=2,languages=['en'],lines_per_video=2):
        self.key=key
        self.wordrange=wordrange
        self.capitalize=capitalize
        self.whitelist=whitelist
        self.blacklist=blacklist
        self.randomness=randomness
        self.languages=languages
        self.lines_per_video=lines_per_video
        self.genLine=self.lineGenerator()
        
    def getVideo(self):
        randomstr=''.join([random.choice(ascii_lowercase) for i in range(self.randomness)])
        results=json.loads(urlopen("https://www.googleapis.com/youtube/v3/search?&key={key}&part=id&maxResults=50&order=date&q={randomstr}&type=video&videoCaption=closedCaption&fields=items/id/videoId".format(key=self.key,randomstr=randomstr)).read())
        id=random.choice(results['items'])['id']['videoId']
        return id
    
    def getLang(self,id):
        results=urlopen('http://www.youtube.com/api/timedtext?v={id}&expire=1&type=list'.format(id=id)).read()
        try:
            tree=ET.fromstring(results)
        except ET.ParseError:
            raise NoSuitableText
        languages=[{'lang_code':track.attrib['lang_code'],'name':track.attrib['name']} for track in tree.findall('track')]
        for language in languages:
            if language['lang_code'] in self.languages:
                return language
        raise NoSuitableText
    
    def getLines(self,id,lang):
        results=urlopen('http://www.youtube.com/api/timedtext?v={id}&expire=1&lang={lang}&name={name}'.format(id=id,lang=lang['lang_code'],name=lang['name'])).read()
        try:
            tree=ET.fromstring(results)
        except ET.ParseError:
            raise NoSuitableText
        alllines=[capitalize(HTMLParser().unescape(Poet.stripbeginnonletters(line.text.replace('\n','')))) for line in tree.findall('text') if not Poet.isnothing(line.text) and only_roman_chars(unicode(line.text)) and len(line.text.split()) in self.wordrange]
        alllines=self.filterBlacklist(self.filterWhitelist(alllines))
        
        if len(alllines)==0:
            raise NoSuitableText
        elif len(alllines)<self.lines_per_video:
            lines=alllines
        else:
            lines=random.sample(alllines,self.lines_per_video)
        return lines
    
    def lineGenerator(self):
        linecache=[]
        while True:
            if len(linecache)>0:
                yield linecache.pop(0)
            else:
                try:
                    id=self.getVideo()
                    lang=self.getLang(id)
                    lines=self.getLines(id,lang)
                except NoSuitableText:
                    continue
                linecache.extend(lines[1:])
                yield lines[0]
        
    def filterWhitelist(self, lines):
        return [line for line in lines if not self.whitelist or any([line.__contains__(whitelistentry) for whitelistentry in self.whitelist])]
    
    def filterBlacklist(self, lines):
        return [line for line in lines if not any([line.__contains__(blacklistentry) for blacklistentry in self.blacklist])]
        
    def makePoem(self,number_of_lines):
        poemlist=[self.genLine.next() for i in xrange(number_of_lines)]
        random.shuffle(poemlist)
        poem='\n'.join(poemlist)
        return poem

        
def strip_html(text):
    return re.sub('<[^<]+?>', '', text)

try:
	WHITELIST
except NameError:
	WHITELIST=[]

try:
	BLACKLIST
except NameError:
	BLACKLIST=[]
		
p=Poet(YOUTUBE_KEY,WORDRANGE,CAPITALIZE, WHITELIST, BLACKLIST, lines_per_video=MAX_LINES_PER_VIDEO)

for i in range(NUMBER_OF_POEMS):
    poem=strip_html(p.makePoem(POEM_LENGTH)).encode('utf-8')
    OUTPUTHANDLER(poem, OUTPUTHANDLERSETTINGS)