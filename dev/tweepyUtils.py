
from __future__ import print_function
import sys
sys.path = sys.path[:7] + sys.path[9:] + sys.path[7:9]
from PySocial_Twitter import twitStream
import json
import glob
from os.path import join
import numpy as np
#from datetime import date
import datetime as dt
from config_all import *
import configparser
from datetime import date
import os
import errno


#For this files, tweets must be in the specific keywords and be geotagged

#def jsonfile_ondata_handler(data, directory, filepostfix):
#    tweet = json.loads(data)
#    if 'text' in tweet.keys():
#        if any(word in tweet['text'] for word in track):
#            filename = join(directory, date.today().isoformat() + '_' + filepostfix + '.json')
#            with open(filename,'a') as f:
#                f.write(data)
#    return True


def make_directory(countyName, date):
    outdirectory = pathRoot + '/data/output/' + countyName +\
        '/tweetStreams/' + date
    return outdirectory

def grabTweets(countyname, usetrack=False, verbose=False):
    configs = configparser.ConfigParser()
    configfile = workDIR + "/" + 'config_' + countyname + ".cfg"
    configs.read(configfile)
    print (configs)
    outdirectory = make_directory(countyname, date.today().isoformat())
    if not os.path.isdir(outdirectory):
        try:
            os.makedirs(os.path.dirname(outdirectory))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    kwargs = {}
    #for k in configs['KWARGS'].keys():
    #    print (k)
    #    kwargs[k] = configs['KWARGS'][k]
    kwargs['directory'] = outdirectory
    
    for k in configs.options('KWARGS'):
        kwargs[k] = configs.get('KWARGS', k)
        
    track = [configs.get('TRACK', i) for i in configs.options('TRACK')]
    

    def jsonfile_ondata_handler(data, directory, filepostfix):
        tweet = json.loads(data)
        if 'text' in tweet.keys():
            if any(word in tweet['text'] for word in track):
                filename = join(directory, date.today().isoformat() + 
                            '_' + filepostfix + '.json')
                with open(filename,'a') as f:
                    f.write(data)
                
        return True

    ondata_handler = jsonfile_ondata_handler
    #just to be sure about the sorting creating an argsort from the keys

    if usetrack:
        locations = None
        thistrack = track
    else:
        thistrack = None
        locations = [configs.get('LOCATIONS', i) for i in configs.options('LOCATIONS')]

    twitStream(consumer_key = consumer_key,
               consumer_secret = consumer_secret,
               access_token = access_token,
               access_secret = access_secret,
               ondata_handler = ondata_handler, #function direction where to send data
               track = thistrack, #None default value
               locations = locations, #None default value
               verbose = verbose, #Display extra messages
               **kwargs)
    

