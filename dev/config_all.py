"""
This script is used by all other scripts.
Filepaths and general keywords are stored here.
"""

#pathRoot is the directory in which the project is stored
# Using an environmental variable is preferred
#pathRoot = '/gws/projects/project-tweetpdsentiment/workspace/share'
pathRoot = '/nfshome/pa1303'

#outdirectory = pathRoot + '/test'

summarydir = 'summaries'

#outdirectory = pathRoot + '/data/output/' + countyName + '/tweetStreams/' + date

workDIR = pathRoot + "/tweetsPDsentiment/"

inputDIR = pathRoot + "/tweetsPDsentiment/inputs"

track = ["police", "pd", "law", "cop", "laws", "cops"] #track is used to create location specific keywords
    
general_track = ["police", "law", "cop", "law enforcement", 
                 "criminal justice", "laws", "cops", "lawyers",
                 "district attorney", "da", "district attorneys", "das", "lawyer", "legal", 
                 "court", "peace", "trial", "courts", "prisons",
                 "jail", "prison", "probation", "parole", 
                 "policing", "crime", "squad", "pigs",
                 "5-0", "squad", "crimes", "jails", "judge","judges"] #general keywords


