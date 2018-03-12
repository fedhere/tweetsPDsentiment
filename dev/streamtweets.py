from __future__ import print_function
from tweepyUtils import grabTweets
import sys


if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print ('''Usage: 
python keyword_gen.py <place> place needs to be one of the keywords in jurisdictions.py
All names in coords.py are formatted as <county-or-city-name>_<state> all lower case''')
        sys.exit()
        
    for arg in sys.argv[1:]:
        loc = arg    
        loc_gkw = loc + "_gkw"
        

        grabTweets(loc, loc, usetrack=True)
        print ("hello")
        grabTweets(loc, loc_gkw, usetrack=False)
