TUMBLR_REQUEST_TOKEN_URL="http://www.tumblr.com/oauth/request_token"
TUMBLR_AUTHORIZE_URL="http://www.tumblr.com/oauth/authorize"
TUMBLR_ACCESS_TOKEN_URL="http://www.tumblr.com/oauth/access_token"

from rauth import OAuth1Service as oa
import webbrowser
import re
from time import sleep
import pytumblr
from datetime import datetime

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
    
    def post(self,body,title='',publishdate=None):
        if publishdate is None:
            self.tumblr.create_text(self.blogname,title=title,body=body)
        else:
            self.tumblr.create_text(self.blogname,title=title,body=body,state="queue",publish_on=publishdate)