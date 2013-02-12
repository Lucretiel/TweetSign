'''
Created on Jan 7, 2013

@author: nathan
'''

from tweepy import StreamListener, OAuthHandler, Stream
import requests
import functools

import keys #THIS IS NOT IN GITHUB

class DeadSimpleSign:
    def __init__(self, host='10.42.0.60', port=39999):
        self.url_template = 'http://{}:{}/dead-simple/'.format(host, port) + '{}'

    def is_ready(self):
        result = requests.get(self.url_template.format('isready'))
        result.raise_for_status()
        return result.json()['ready']

    def reset(self):
        requests.get(self.url_template.format('reset')).raise_for_status()

    def _send(self, text, color, mode, label):
        payload = {'text': text}
        if color is not None:
            payload['color'] = color
        if mode is not None:
            payload['mode'] = mode
        if label is not None:
            payload['label'] = label

        requests.get(self.url_template.format('send'), params=payload).raise_for_status()

    def set_text(self, text, color=None, mode=None):
        self._send(text, color, mode, None)

    def set_label(label, text, color=None):
        self._send(text, color, None, label)

sign = DeadSimpleSign()

def validate_sign():
    print 'Validating Sign'

    if not sign.is_ready():
        print 'Sing is not ready. Resetting...'
        sign.reset()

class SignListener(StreamListener):
    def on_status(self, status):
        print "Got a tweet!"
        print "  username: %s" % status.user.screen_name
        print "  tweet: %s" % status.text

        if 'mimedia' not in status.text.lower():
            print "Huh. 'mimedia' wasn't found in that tweet. Oh well."
            return True

        text = '{}{}: {}{}'.format('{red}', status.user.screen_name, '{green}', status.text)
        sign.set_text(text)

if __name__ == '__main__':
    validate_sign()

    listener = SignListener()
    auth = OAuthHandler(keys.consumer_key, keys.consumer_secret)
    auth.set_access_token(keys.access_token, keys.access_token_secret)

    stream = Stream(auth, listener)
    stream.filter(track=['mimedia'])
