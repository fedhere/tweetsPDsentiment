"""
This script initializes the data collection.
There are two processes for a location.
p1 collects tweets based on location specific keywords
p2 collects tweets based on the coordinates of the location
and gets anything relevant to criminal justice.

"""

from __future__ import print_function
from tweepyUtils import grabTweets
import sys
import os
from config_all import *
from multiprocessing import Process

#loc is the location name.
loc = sys.argv[1]
loc_gkw = loc + '_gkw'

p2 = Process(target = grabTweets, args=(loc, loc_gkw, False,))
p2.start()
p1 = Process(target = grabTweets, args=(loc, loc, True,))
p1.start()

