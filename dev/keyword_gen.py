from __future__ import print_function
import sys
import os
import string
from datetime import datetime
import ConfigParser

from config_all import *

sys.path.append(inputDIR)
#from coords import coords
from jurisdictions import juris_dict

def get_keys(line):
    line = line.replace('\n', '')
    line = line.split(',')
    return line

def genplace_all(placeName, keys):
    '''generates keywords for a place'
    placeName (str): the name of the place as it appears on the coordinates file
    keys (dataFrame): a row in a dataframe made from the keys.csv file. It
                   contains the api keys for the lcoation
    '''

    tmp = juris_dict[placeName]
    tmp['state'] = placeName.split('_')[-1].upper()
    tmp['name'] = ' '.join(placeName.split('_')[:-1])
    tmp['name'] = tmp['name'].title()
    handles = None
    if tmp['handles']:
        handles = tmp['handles']

    print (tmp)
    
    #creates a configuration file using location specific keywords
    generate(tmp['name'], tmp['coords'], tmp['keywords'], keys, state=tmp['state'], 
             short=tmp['short'], handles=handles, verbose=True)
    
    #creates a configuration file that uses general keywords in a set of coordinates
    generate(tmp['name'], tmp['coords'], tmp['keywords'], keys, state=tmp['state'], 
             short=tmp['short'], gkw=True, verbose=True)
    


def generate(location, coords, kw, apikeys, handles=None, state=None, short=None, 
             gkw=False, verbose=False):
    """
    This function creates a configuration file 
    
    location (str) - The location of the data being collected. This is 
         necessary in order to name the config file correctly
         
    coords (list)- The coordinates of the location to add to the config file
    
    kw (list) - keywords specific to a location
    
    apikeys (dataframe) - contains tweepy authorization keys for the location
    
    handles (list) - contains twitter handles important to a location
    
    state (str) - state in which the location is, needed to generate file names

    short (str)- aks if there is a short version of the location name in order
        to create a keyword with the short (default None)
        
        
    gkw (bool) - general keywords. if True creates a config file with gkw instead of location  specific keywords (default False)
    
    verbose (bool) - if True, it prints where configuration files are being saved
         
    """
    

    parser = ConfigParser.SafeConfigParser()
    #regenerate file name
    placeName = '_'.join(location.split(' ') + [state]).lower()    

    new_track = []
    if not gkw:
        # track is defined in config_all.py
        for words in track:
            print (words)
            new_track.append(location + ' ' + words)
            new_track.append(location + words)
            new_track.append(location.upper() + ' ' + words.upper())
            new_track.append(location.upper() + words.upper())
            new_track.append(location.title() + words.title())
        
        
        if not short is None:
            for words in track:
                new_track.append(short + ' ' + words)
                new_track.append(short + words)
        if not handles is None:
            new_track = new_track + handles
            
        new_track = new_track + kw
                
    else:
        placeName = placeName + '_gkw'
        for w in general_track:
            new_track.append(w)
            new_track.append(w.upper())
            new_track.append(w.title())
    
    #adds sections for the config file
    parser.add_section('API')
    
    parser.set('API', 'consumer_key', apikeys["API Key"].values[0])
    parser.set('API', 'consumer_secret', apikeys["API Secret"].values[0])
    parser.set('API', 'access_token', apikeys["Access token"].values[0])
    parser.set('API', 'access_secret', apikeys["Access token secret"].values[0])
    
    parser.add_section('KWARGS')
    parser.set('KWARGS', 'filepostfix', placeName)
    
    parser.add_section('TRACK')
    for i in range(len(new_track)):
        parser.set('TRACK', 'r' + str(i+1), new_track[i])
        
    parser.add_section('LOCATIONS')
    
    for i in range(len(coords)):
        parser.set('LOCATIONS', 'loc' + str(i+1), str(coords[i]))
    
    parser.add_section('DATE')
    parser.set('DATE', 'date', datetime.today().isoformat())

    outfile = inputDIR + '/placeConfigs/' + placeName + ".cfg"
    
    #saves date of older configuration files
    cmd = "mv " + outfile.replace(' ','\ ') + ' ' + \
                  outfile.replace(' ','\ ') + '_' + datetime.today().isoformat()
    if os.path.isfile(outfile):
        os.system(cmd) 
    f = open(outfile, 'w')
    
    if verbose: 
        print ("saving tweet searche keywords in ", outfile)
    parser.write(f)
    
    return
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ('''Usage: 
python keyword_gen.py <place1> (<place2> ... as many as you want, min 1)
where place needs to be one of the keywords in jurisdictions.py
All names in coords.py are formatted as <county-or-city-name>_<state> all lower case''')
        sys.exit()
    key_path = pathRoot + '/tweetsPDsentiment/inputs/keys.csv'
    import pandas as pd
    f = pd.read_csv(key_path)
    
    
    for place in sys.argv[1:]:
        genplace_all(place ,f[f.jurisdiction == place])
