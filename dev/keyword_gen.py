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

def genplace_all(placeName):
    '''generates keywords for a place'
    placeName (str): the name of the place as it appears on the coordinates file
    '''

    tmp = juris_dict[placeName]
    tmp['state'] = placeName.split('_')[-1].upper()
    tmp['name'] = ' '.join(placeName.split('_')[:-1])
    tmp['name'] = tmp['name'].title()
    handles = None
    if tmp['handles']:
        handles = tmp['handles']

    print (tmp)
    generate(tmp['name'], tmp['coords'], tmp['state'], 
             short=tmp['short'], handles, verbose=True)
    
    generate(tmp['name'], tmp['coords'], tmp['state'], 
             short=tmp['short'],gkw=True, verbose=True)
    


def generate(location, coords, handles=None, state=None, short=None, 
             gkw=False, verbose=False):
    """
    This function creates a config file 
    
    location (str) - The location of the data being collected. This is 
         necessary in order to name the config file correctly
         
    coords - The coordinates of the location to add to the config file
    
    state (str) - state in which the location is, needed to generate file names

    short (str)- aks if there is a short version of the location name in order
        to create a keyword with the short (default None)
        
    gkw (bool) - general keywords. if True creates a config file with gkw instead of location  specific keywords (default False)
         
    """
    
    parser = ConfigParser.SafeConfigParser()
    #regenerate file name
    placeName = '_'.join(location.split(' ') + [state]).lower()    

    new_track = []
    if not gkw:
        
        for words in track:
            new_track.append(location + ' ' + words)
            new_track.append(location + words)
            new_track.append(location.upper() + ' ' + words.upper())
            new_track.append(location.upper() + words.upper())
            new_track.append(location.title() + words.title())
        
        
        if not short is None:
            for words in track:
                new_track.append(short + ' ' + words)
                new_track.append(short + words)
                
        new_track = new_track + handles
                
    else:
        placeName = placeName + '_gkw'
        for w in general_track:
            new_track.append(w)
            new_track.append(w.upper())
            new_track.append(w.title())
    
    #adds sections for the config file

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
    if os.path.isfile(outfile):
        os.system("mv " + outfile + ' ' + 
                  outfile + '_' + datetime.today().isoformat()) 
    f = open(outfile, 'w')
    
    if verbose: 
        print ("saving tweet searche keywords in ", outfile)
    parser.write(f)
    
    return
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ('''Usage: 
python keyword_gen.py <place1> (<place2> ... as many as you want, min 1)
where place needs to be one of the keywords in coords.py
All names in coords.py are formatted as <county-or-city-name>_<state> all lower case''')
        sys.exit()
    for place in sys.argv[1:]:
        genplace_all(place)
