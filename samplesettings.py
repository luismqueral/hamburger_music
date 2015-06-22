#Sample settings file. Rename to "settings.py" to use.
from os import path
from datetime import timedelta

POEM_LENGTH=5

MINSUBLENGTH=3 #Minimum length in characters for a caption
MAX_LINES_PER_VIDEO=2 #Setting this to a higher number gives higher performance, but more lines from the same video
NUMBER_OF_POEMS=50 #Use this to make large amounts of poems
WORDRANGE=xrange(3,6) #Anywhere from 1 to 7 words.
#WORDRANGE=[1,3,7,8] #Only lines with either 1,3,7, or 8 words are accepted
#WORDRANGE=[6] #Only lines with 6 words are accepted
CAPITALIZE=True

#######################################################
YOUTUBE_KEY="####"
#######################################################


#################  Filter #############################

# Leave empty, comment, or remove to disable whitelist
WHITELIST=[
'awesome',
'I\'m hungry',
'driveway'
]
#WHITELIST=open('/path/to/whitelist.txt').read().splitlines()     # Uncomment to read newline-separated whitelist-entries from file

# Leave empty, comment, or remove line to disable blacklist
BLACKLIST=[
'New York',
'Los Angeles',
'don\'t mess with me'
]
#BLACKLIST=open('/path/to/blacklist.txt').read().splitlines()     # Uncomment to read newline-separated blacklist-entries from file


