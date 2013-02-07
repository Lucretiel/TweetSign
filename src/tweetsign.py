'''
Created on Jan 7, 2013

@author: nathan
'''

from tweepy import StreamListener, OAuthHandler, Stream
import json
import httplib
import urllib

import keys #THIS IS NOT IN GITHUB

def validate_sign():
    print 'Validating Sign'
    connection = httplib.HTTPConnection('localhost', 39999)
    connection.request('GET', '/dead-simple/isready')
    result = json.loads(connection.getresponse().read())

    if not result['ready']:
        print 'Sing is not ready. Resetting...'
        request = '/dead-simple/reset'
        print request
        connection.request('GET', request)
        response = connection.getresponse()
        if response.status >= 400:
            raise RuntimeError('Error resetting sign', response)
        print response.read()

    request = '/dead-simple/send?text={red}{a}: {green}{b}'
    print request
    connection.request('GET', request)
    response = connection.getresponse()
    if response.status >= 400:
        raise RuntimeError('Error resetting sign', response)
    print response.read()
    connection.close()

class SignListener(StreamListener):
    def on_status(self, status):
        print "Got a tweet!"

        labels = ('a', 'b')
        data = (status.user.screen_name, status.text)

        connection = HTTPConnection('localhost', 39999)
        for label, data in zip(labels, data):
            params = {'label': label, 'data': data}
            request = '/dead-simple/send?' + urllib.urlencode(params)
            print request
            connection.request('GET', request_template % request_params)
            result = connection.getresponse()
            print result.read()
            connection.close()

if __name__ == '__main__':
    validate_sign()

    listener = SignListener()
    auth = OAuthHandler(keys.consumer_key, keys.consumer_secret)
    auth.set_access_token(keys.access_token, keys.access_token_secret)

    stream = Stream(auth, listener)    
    stream.filter(track=['mimedia'])