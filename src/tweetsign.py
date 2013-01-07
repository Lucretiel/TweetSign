'''
Created on Jan 7, 2013

@author: nathan
'''

from tweepy import StreamListener, OAuthHandler, Stream
import json
import httplib

import keys #THIS IS NOT IN GITHUB

class SignListener(StreamListener):
    def on_status(self, status):
        print "Got a tweet!"
        text = status.text
        if '#mimedia' not in text:
            print "  This tweet did not contain #mimedia..."
            print "  Here's the tweet %s" % text
            return True
        
        message = {'text': '{red}{user}: {green}{tweet}',
                   'name': 'tweet',
                   'temporary': True,
                   'fields': {'user': {'text': status.user.screen_name},
                              'tweet': {'text': text}}}
        print "Assembled message %s" % message
        message = json.dumps(message)
        connection = httplib.HTTPConnection('localhost', 39999)
        headers = {'Content-Type': 'application/json'}
        print "  Sending request..."
        connection.request('POST', '/sign-controller/clumps/', message, headers)
        result = connection.getresponse()
        if result.status >= 400:
            print "There was an error"
            return True
        clump_id = result.read()
        print "Created message with ID %s" % clump_id
        print "  Displaying..."
        message = json.dumps({'ID': clump_id})
        print "  Sending request..."
        connection.request('PUT', '/sign-controller/active-clump', message, headers)

if __name__ == '__main__':
    listener = SignListener()
    auth = OAuthHandler(keys.consumer_key, keys.consumer_secret)
    auth.set_access_token(keys.access_token, keys.access_token_secret)

    stream = Stream(auth, listener)    
    stream.filter(track=['mimedia'])