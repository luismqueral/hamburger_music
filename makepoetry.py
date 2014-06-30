from os import path
####################################################

POEM_LENGTH=10

MINSUBLENGTH=3 #Minimum length in characters for a caption
MAX_LINES_PER_VIDEO=2 #Setting this to a higher number gives higher performance, but more lines from the same video
SAVE_TO_FILE=True  #Set to False to output to stdout
POEM_BASENAME="Poem-" #The current date and time get added to POEM_BASENAME, so for example Poem-2014-06-30T12.51.txt
POEM_EXTENSION=".txt"
POEM_PATH="/home/elon/poems"
NUMBER_OF_POEMS=1 #Use this to make large amounts of poems

#######################################################
YOUTUBE_KEY="AIzaSyCHglmxmC_NSLeFdLwXUgiox2RveFbSms0"
#######################################################
import json
from urllib import urlopen
from string import ascii_lowercase
import random
import xml.etree.ElementTree as ET
from HTMLParser import HTMLParser
from datetime import datetime


class NoSuitableText(Exception):
    pass


class Poet(object):
    nothing=[None,'',' ']
    @staticmethod
    def isnothing(item):
        return item in Poet.nothing or len(item)<MINSUBLENGTH
    
    def __init__(self,key,randomness=2,languages=['en'],lines_per_video=2):
        self.key=key
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
        alllines=[line.text.replace('\n','') for line in tree.findall('text') if not Poet.isnothing(line.text)]
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
        
    
    def makePoem(self,number_of_lines):
        poemlist=[self.genLine.next() for i in xrange(number_of_lines)]
        random.shuffle(poemlist)
        poem='\n'.join(poemlist)
        return poem

        
        
p=Poet(YOUTUBE_KEY,lines_per_video=MAX_LINES_PER_VIDEO)

for i in range(NUMBER_OF_POEMS):
    if SAVE_TO_FILE:
        filename=path.join(POEM_PATH,POEM_BASENAME+datetime.now().isoformat()[:-7].replace(':','.')+POEM_EXTENSION)
        with open(filename,'w') as f:
            f.write(HTMLParser().unescape(p.makePoem(POEM_LENGTH)).encode('utf-8'))
    else:
        print HTMLParser().unescape(p.makePoem(POEM_LENGTH)).encode('utf-8')