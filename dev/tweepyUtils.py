
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



def make_directory(countyName, date):
    """
    Creates a directory name
    
    countyName - part of the name of the directory
    
    date - date of the directory  being created
    
    """
    
    #pathRoot is taken from the config_all file
    
    outdirectory = pathRoot + '/data/output/' + countyName + '/tweetStreams/' + date
    return outdirectory

def grabTweets(countyname, configname, usetrack=False, verbose=False):
    """
    Saves the tweets in a json file.
    
    
    """
    
    configs = configparser.ConfigParser()
    configfile = inputDIR + "/placeConfigs/" + 'config_' + configname + ".cfg"
    configs.read(configfile)
    print (configs)
    outdirectory = make_directory(countyname, date.today().isoformat())
    if not os.path.isdir(outdirectory):
        try:
            os.makedirs(outdirectory)
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
    print(track)
    

    #just to be sure about the sorting creating an argsort from the keys

    if usetrack:
        locations = None
        thistrack = track


    else:
        thistrack = None
        locations = [configs.get('LOCATIONS', i) for i in configs.options('LOCATIONS')]
        
        
    def jsonfile_ondata_handler(data, directory, filepostfix):
        tweet = json.loads(data)
        if usetrack:
            filename = join(directory, date.today().isoformat() + '_' + filepostfix + '.json')
            with open(filename,'a') as f:
                f.write(data)
        else:   
            if 'text' in tweet.keys():
                if any(word in tweet['text'] for word in track):
                    filename = join(directory, date.today().isoformat() + '_' + filepostfix + '.json')
                    with open(filename,'a') as f:
                        f.write(data)
                    
        return True
    

    ondata_handler = jsonfile_ondata_handler

    twitStream(consumer_key = consumer_key,
               consumer_secret = consumer_secret,
               access_token = access_token,
               access_secret = access_secret,
               ondata_handler = ondata_handler, #function direction where to send data
               track = thistrack, #None default value
               locations = locations, #None default value
               verbose = verbose, #Display extra messages
               **kwargs)


