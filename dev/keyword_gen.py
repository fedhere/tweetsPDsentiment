from __future__ import print_function
import ConfigParser
from config_all import *

parser = ConfigParser.SafeConfigParser()

def generate(location, coords, short=None, gkw=False, verbose=False):
    """
    This function creates a config file 
    
    location (str) - The location of the data being collected. This is 
         necessary in order to name the config file correctly
         
    coords - The coordinates of the location to add to the config file
    
    short (str)- aks if there is a short version of the location name in order
        to create a keyword with the short
        
    gkw - general keywords. creates a config file with gkw instead of location
        specific keywords
         
    """
    
    
    track = ["police", "pd", "law", "cop"] #track is used to create location specific keywords
    
    general_track = ["police", "law", "cop", "law enforcement", 
                     "criminal justice",
                     "district attorney", "da", "lawyer", "legal", 
                     "court", "peace", "trial",
                     "jail", "prison", "probation", "parole", 
                     "policing", "crime", "squad", "pigs",
                     "5-0", "squad"] #general keywords
                     
    new_track = []
    if gkw:
        for i in track:
            new_track.append(location + ' ' + i)
            new_track.append(location + i)
        
    
        if not short is None:
            for i in track:
                new_track.append(location + ' ' + i)
                new_track.append(location + i)
                
    else:
        new_track = general_track
    
    #adds sections for the config file
    parser.add_section('KWARGS')
    parser.set('KWARGS', 'filepostfix', location)
    parser.add_section('TRACK')
    for i in range(len(new_track)):
        
        parser.set('TRACK', 'r' + str(i+1), new_track[i])
        
    parser.add_section('LOCATIONS')
    
    for i in range(len(coords)):
        parser.set('LOCATIONS', 'loc' + str(i+1), str(coords[i]))
        
    outfile = workDIR + "/inputs/" + 'config_' + location + ".cfg"
    f = open(outfile, 'w')
    
    if verbose: 
        print ("saving tweet searche keywords in ", outfile)
    parser.write(f)
    
    return
    
