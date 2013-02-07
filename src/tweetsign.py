'''
Created on Jan 7, 2013

@author: nathan
'''

from tweepy import StreamListener, OAuthHandler, Stream
import json
import httplib

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
    print connection.getresponse().read()
    connection.close()

class SignListener(StreamListener):
    def on_status(self, status):
        print "Got a tweet!"

        request_template = '/dead-simple/send?label=%s&text=%s'

        labels = ('a', 'b')
        data = (status.user.screen_name, status.text)

        connection = HTTPConnection('localhost', 39999)
        for request_params in zip(labels, data):
            request = request_template % request_params
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