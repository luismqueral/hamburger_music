from . import handlers.post_to_tumblr

def print_to_terminal(poem, settings):
    print(poem)
    print()


def write_to_file(poem, settings):
    from os import path
    from datetime import datetime

    filename = path.join(settings['POEM_PATH'],
                         settings['POEM_BASENAME'] + datetime.now().isoformat()[:-7].replace(':', '.') + settings[
                             'POEM_EXTENSION'])
    with open(filename, 'w') as f:
        f.write(poem)
        f.write("\n")


def post_to_tumblr(poem, settings):

    t = handlers.post_to_tumblr.Tumblr(settings['CONSUMER_KEY'], settings['CONSUMER_SECRET'], settings['BLOGNAME'],
                                       settings['OAUTHFILE'])
    t.post(poem, title='', publishdate=None)  # TODO: Add support for publishdate (timedelta)
