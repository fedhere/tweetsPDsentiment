from __future__ import print_function
from datetime import datetime as dt
from dateutil import parser
import random
import json

#IO stuff
import sys
from os.path import isfile, dirname, basename
try:
    import cPickle as pickle
except:
    import pickle

#Necessary Imports for streaming API
import sys, time
from tweepy import StreamListener, OAuthHandler
from tweepy.streaming import Stream


#Twitter API Funs
def twitAuth(consumer_key, consumer_secret, access_token, access_secret):
    auth = OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_secret)
    return auth

def twitStream(consumer_key,
               consumer_secret,
               access_token,
               access_secret,
               ondata_handler, #function direction where to send data
               track = None, #None default value
               locations = None, #None default value
               verbose = False,
               **kwargs):

    auth = twitAuth(consumer_key,consumer_secret,access_token,access_secret)

    class CustomStreamListener(StreamListener):
        def on_data(self, data):
            return ondata_handler(data, **kwargs)

        def on_exception(self,status_code):
            print('Exception %s sent during stream.' % status_code)
            return True

        def on_error(self, status_code):
            print('Exception %s sent during stream.' % status_code)
            if 400 <= status_code < 500:
                print('Allocation issues. Pausing...', file=sys.stderr)
                time.sleep(920)
                return True #Try again after 15 minutes
            ## print error to sys.stderr file (using >> formating, for python 2.x)
            print('Encountered error with status code: %s' % status_code, file = sys.stderr)
            return True # Don't kill the stream

        def on_timeout(self):
            ## print error to sys.stderr file (using >> formating, for python 2.x)
            print('Timeout...', file = sys.stderr)
            return True # Don't kill the stream


    while True:
        try:
            sapi = Stream(auth, CustomStreamListener())
            sapi.filter(track = track, locations = locations)

        except:
            time.sleep(60)
            pass


##########
