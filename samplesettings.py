#Sample settings file. Rename to "settings.py" to use.

POEM_LENGTH=5

MINSUBLENGTH=3 #Minimum length in characters for a caption
MAX_LINES_PER_VIDEO=2 #Setting this to a higher number gives higher performance, but more lines from the same video
SAVE_TO_FILE=True  #Set to False to output to stdout
POEM_BASENAME="Poem-" #The current date and time get added to POEM_BASENAME, so for example Poem-2014-06-30T12.51.txt
POEM_EXTENSION=".txt"
POEM_PATH="/path/to/poetry/dir/"
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


