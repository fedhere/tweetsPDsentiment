import os
import pandas as pd
from config_all import *
from tweepyUtils import grabTweets

def check_pid():        
    """ Check For the existence of a unix pid. """
    df = pd.read_csv(inputDIR + '/pids.csv', header=None, names=['pid', 'name'])
    for i in range(df.shape[0]):
        pid = df.iloc[i, 0]
        try:
            os.kill(pid, 0)
        except OSError:
            name = df.iloc[i, 1]
            if 'gkw' in name:
                loc = name[:-4]
                grabTweets(loc, name, False)
            else:
                grabTweets(name, name, True)
                
            df = df.drop(df.index[i])
            df.to_csv(inputDIR + '/pids.csv', header = False)
                
            print('dead')
            return False
            
        else:
            print('alive')
            #return True
        
check_pid()