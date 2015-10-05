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

from libpoetry import Poet

try:
    from settings import *
except ImportError:
    exit(
        "Error, no settings-file found. Create a settings.py file, or edit and rename samplesettings.py to settings.py")



if __name__ == '__main__':

    try:
        WHITELIST
    except NameError:
        WHITELIST = []

    try:
        BLACKLIST
    except NameError:
        BLACKLIST = []

    p = Poet(YOUTUBE_KEY, WORDRANGE, CAPITALIZE, WHITELIST, BLACKLIST, lines_per_video=MAX_LINES_PER_VIDEO)

    for i in range(NUMBER_OF_POEMS):
        poem = p.makePoem(POEM_LENGTH)
        OUTPUTHANDLER(poem, OUTPUTHANDLERSETTINGS)
