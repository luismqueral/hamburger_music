#Configure your OS to run this script at startup. It'll track POEM_PATH for any new files, 
#and upload the contents to Tumblr. If you're having trouble with the script, remove or rename OAUTHFILE
#and reauthenticate


from os import path
#######################################

BLOGNAME='hamburgermusic' #If your tumblr is foobar.tumblr.com, your blogname is "foobar" 
OAUTHFILE=path.join(path.expanduser('~'),'.tumblr.oauth') #Comment this out and uncomment the next line to specify a path other than your homedir
#ACCESS_TOKEN_STORAGE_FILE='/path/to/file.oauth'
POEM_PATH='/Users/luis/Dropbox/Public/poems'

###########################################
CONSUMER_KEY='gcXNyTsZCHfH1ROf519M3jwHfAbSWNMawSV7PW1FrKCm6KtIJj'
CONSUMER_SECRET='j7akedGujJcKoIEymKbZJb8WYkM4pmX9t1u3imnRIaYxcFP06s'

TUMBLR_REQUEST_TOKEN_URL="http://www.tumblr.com/oauth/request_token"
TUMBLR_AUTHORIZE_URL="http://www.tumblr.com/oauth/authorize"
TUMBLR_ACCESS_TOKEN_URL="http://www.tumblr.com/oauth/access_token"
###################################################################

from rauth import OAuth1Service as oa
import webbrowser
import re
from time import sleep
import pytumblr
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sys import exit
import signal


class NewPoemHandler(FileSystemEventHandler):
    def __init__(self,tumblr):
        self.tumblr=tumblr
        
    def on_created(self,event):
        if not event.is_directory:
            with open(event.src_path) as f:
                self.tumblr.post(f.read())
    
    def on_moved(self,event):
        self.on_created(event)
    
    def on_modified(self,event):
        self.on_created(event)


class Tumblr(object):
    requesturl=TUMBLR_REQUEST_TOKEN_URL
    authorizeurl=TUMBLR_AUTHORIZE_URL
    accesstokenurl=TUMBLR_ACCESS_TOKEN_URL
    def __init__(self,ck,cs,blogname,atlocation):
        self.ck=ck
        self.cs=cs
        self.blogname=blogname
        try:     
            with open(atlocation,'r') as f:
                contents=f.read()
            if len(contents)<50 or len(contents)>150:
                raise ValueError
            self.at,self.ats=contents.split('\n')
        except IOError,ValueError:
            self.at,self.ats=self.gettokens()
            with open(atlocation,'w') as f:
                f.write(self.at)
                f.write('\n')
                f.write(self.ats)
        
        self.tumblr=pytumblr.TumblrRestClient(
                                     self.ck,
                                     self.cs,
                                     self.at,
                                     self.ats)
    
    def gettokens(self):
        tumblr=oa(
                  name='tumblr',
                  consumer_key=self.ck,
                  consumer_secret=self.cs,
                  request_token_url=Tumblr.requesturl,
                  access_token_url=Tumblr.accesstokenurl,
                  authorize_url=Tumblr.authorizeurl)
        request_token, request_token_secret=tumblr.get_request_token()
        authorize_url=tumblr.get_authorize_url(request_token)
        webbrowser.get().open(authorize_url)
        print 'Authorizing application now. Please click "Accept", and then copy the url you get sent to and paste it here'
        sleep(1)
        print '\n'*5
        print 'Authorizing application now. Please click "Accept", and then copy the url you get sent to and paste it here'
        url=raw_input("url: ")
        oauth_verifier=re.findall('oauth_verifier=(.*)#_=_',url)[0]
        return tumblr.get_access_token(request_token, request_token_secret, params={'oauth_verifier':oauth_verifier})
    
    def post(self,body,title=''):
        self.tumblr.create_text(self.blogname,title=title,body=body)
      
tumblr=Tumblr(CONSUMER_KEY,CONSUMER_SECRET,BLOGNAME,OAUTHFILE)  
handler=NewPoemHandler(tumblr)
observer=Observer()
observer.schedule(handler, POEM_PATH)
print 'Starting observing for file changes in {0} now'.format(POEM_PATH)
observer.start()

def shutdownhandler(x,y):
    print 'Received exit signal'
    observer.stop()
    observer.join()
    print 'Exiting now...'
    exit(0)
    
for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
    signal.signal(sig, shutdownhandler)

while True:
    sleep(1000)