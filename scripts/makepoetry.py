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

from hamburger_music import Poet
import sys

if len(sys.argv) != 2:
    print("Please specify the path to the settings-file on the commandline")
    exit(1)

settings = {}
try:
    exec(compile(open(sys.argv[1], "rb").read(), sys.argv[1], 'exec'), settings)
except:
    print("Error importing settings-file. Please make sure the settings-file is valid")
    raise

p = Poet(settings['YOUTUBE_KEY'], settings['WORDRANGE'], settings['CAPITALIZE'], settings.get('WHITELIST',[]), settings.get('BLACKLIST',[]), lines_per_video=settings['MAX_LINES_PER_VIDEO'])

for i in range(settings['NUMBER_OF_POEMS']):
    poem = p.makePoem(settings['POEM_LENGTH'])
    settings['OUTPUTHANDLER'](poem, settings['OUTPUTHANDLERSETTINGS'])
