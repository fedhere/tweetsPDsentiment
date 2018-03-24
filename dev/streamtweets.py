from __future__ import print_function
from tweepyUtils import grabTweets
import sys
import threading
import os
from config_all import *

pidDIR = workDIR + "pids"

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print ('''Usage: 
python streamtweets.py <place> place needs to be one of the keywords in jurisdictions.py
All names in coords.py are formatted as <county-or-city-name>_<state> all lower case''')
        sys.exit()
    pid = os.getpid()
    threads = []
    threadsgkw = []

    for arg in sys.argv[1:]:
        loc = arg    
        loc_gkw = loc + "_gkw"
        t = threading.Thread(target=grabTweets, args=(loc, loc, True,))
        threads.append(t)
        t.daemon = True
        t.start()
        

        tgkw = threading.Thread(target=grabTweets, args=(loc, loc_gkw, False,))
        threadsgkw.append(tgkw)
        tgkw.daemon = True
        tgkw.start()
        
        filename = os.path.join(pidDIR, arg + '_PID.dat')
        if not os.path.isdir(pidDIR):
            try:
                os.makedirs(pidDIR)
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        # this writes the pid to ../pids/detroit_mi_PID.dat or whatever
        # then you can create a cron job that looks if for every jurisdiction the pid is still alive
        
        with open(filename,'w') as f:
                f.write("%d"%pid)        

#        grabTweets(loc, loc, usetrack=True)
#        print ("hello", pid)
#        grabTweets(loc, loc_gkw, usetrack=False)
