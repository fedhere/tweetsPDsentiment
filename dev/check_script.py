"""
Script for checking existing pids
"""

import os
import pandas as pd
from config_all import *
from tweepyUtils import grabTweets

def check_pid():        
    """ Checks process IDs stored in the file pids.csv. If the pid is dead 
    then check_pid will get the name of the stream that was running and rerun it 
    """
    #creates a dataframe of the pids file
    df = pd.read_csv(inputDIR + '/pids.csv', header=None, names=['pid', 'name'])
    
    #check each pid in the dataframe and rerun a stream if necessary
    for i in range(df.shape[0]):
        pid = df.iloc[i, 0]
        try:
            #returns True if pid is alive
            os.kill(pid, 0)
        except OSError:
            name = df.iloc[i, 1]
            #checks if the stream collected tweets based on keywords or coordinates
            if 'gkw' in name:
                loc = name[:-4]
                grabTweets(loc, name, False)
            else:
                grabTweets(name, name, True)
            #deletes the old pid and saves the csv    
            df = df.drop(df.index[i])
            df.to_csv(inputDIR + '/pids.csv', header = False)
                
            print('dead')
            return False
            
        else:
            print('alive')
            #return True
        
check_pid()