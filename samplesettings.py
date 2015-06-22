#Sample settings file. Rename to "settings.py" to use.
from os import path
from datetime import timedelta

POEM_LENGTH=5

MINSUBLENGTH=3 #Minimum length in characters for a caption
MAX_LINES_PER_VIDEO=2 #Setting this to a higher number gives higher performance, but more lines from the same video
NUMBER_OF_POEMS=5 #Use this to make large amounts of poems
WORDRANGE=xrange(3,6) #Anywhere from 1 to 7 words.
#WORDRANGE=[1,3,7,8] #Only lines with either 1,3,7, or 8 words are accepted
#WORDRANGE=[6] #Only lines with 6 words are accepted
CAPITALIZE=True

#######################################################

YOUTUBE_KEY="####"
#################  Output handler #####################
import outputhandlers

# Once a poem is created, it is sent to the outputhandlers. Outputhandlers are 'independent' pieces of code that take as input a single string (the poem), and then send/post/output that string to for example a website or a file
# Most outputhandlers will need certain settings to be set. outputhandlers.write_to_file needs to know where to store the poems and what to call them, outputhandlers.post_to_tumblr needs Tumblr authentication keys for your account, etc


# Sample configurations for outputhandlers.print, outputhandlers.write_to_file, and outputhandlers.post_to_tumblr. Uncomment to use.

  # # # # # # # A. Print poem to terminal # # # # # # #
OUTPUTHANDLER=outputhandlers.print_to_terminal  # Specifies what happens to the poem once it's created.
OUTPUTHANDLERSETTINGS={ }  # Sample settings for outputhandlers "print_to_terminal". outputhandlers.print_to_terminal doesn't require any settings, so we're leaving it blank

  # # # # # # # B. Write poem to file # # # # # # #
# OUTPUTHANDLER=outputhandlers.write_to_file
# OUTPUTHANDLERSETTINGS={  # Sample settings for outputhandlers "write_to_file"
#    "POEM_BASENAME" : "Poem-",  # The current date and time get added to POEM_BASENAME, so for example Poem-2014-06-30T12.51.txt
#    "POEM_EXTENSION" : ".txt",
#    "POEM_PATH" : "/path/to/poetry/dir/" }

  # # # # # # # C. Post poem to Tumblr # # # # # # #
# OUTPUTHANDLER=outputhandlers.post_to_tumblr
# OUTPUTHANDLERSETTINGS={ #Sample settings for outputhandlers "post_to_tumblr"
    # "BLOGNAME" : "hamburgermusic", #If your tumblr is foobar.tumblr.com, your blogname is "foobar"
    # "OAUTHFILE" : path.join(path.expanduser('~'),'.tumblr.oauth'), #You can specify a directory other than your home-directory by entering the full path in parentheses
    # "USETIMEDELTA" : False,
    # "TIMEDELTA" : timedelta(minutes=15), #For this to work, the timezone of your Tumblr-account needs to be set correctly, and your system time should be accurate
    
    # "CONSUMER_KEY" : '####',
    # "CONSUMER_SECRET" : '####'}


#################  Filter #############################

# Leave empty, comment, or remove to disable whitelist
#WHITELIST=[
#'awesome',
#'I\'m hungry',
#'driveway'
#]
#WHITELIST=open('/path/to/whitelist.txt').read().splitlines()     # Uncomment to read newline-separated whitelist-entries from file

# Leave empty, comment, or remove line to disable blacklist
#BLACKLIST=[
#'New York',
#'Los Angeles',
#'don\'t mess with me'
#]
#BLACKLIST=open('/path/to/blacklist.txt').read().splitlines()     # Uncomment to read newline-separated blacklist-entries from file


