from __future__ import print_function
from tweepyUtils import grabTweets
import sys
import os
from config_all import *
from multiprocessing import Process



loc = sys.argv[1]
loc_gkw = loc + '_gkw'

p2 = Process(target = grabTweets, args=(loc, loc_gkw, False,))
p2.start()
p1 = Process(target = grabTweets, args=(loc, loc, True,))
p1.start()


#grabTweets(loc, loc, True)

#grabTweets(loc, loc_gkw, False)