
#consumer_key = '1F0ULrbBcdxjCEwXVaMOp7zki'
#consumer_secret = 'B56M0Q2e51yApgiJNv43qk2o8t7usAxYixltBej4xJSyGbTMGg'
#access_token = '915237585093562368-ejAFNn7nkkilDFrMqqA6vexZFkB74tz'
#access_secret = 'ry8UEE3R6iLsnW74T6q4Tl3393a99siWhAxzbuYOomKdt'

# def jsonfile_ondata_handler(data, directory, filepostfix):
#    tweet = json.loads(data)
    #if 'text' in tweet.keys():
    #    if any(word in tweet['text'] for word in track):
    #        filename = join(directory, date.today().isoformat() + '_' + filepostfix + '.json')
    #        with open(filename,'a') as f:
    #            f.write(data)
#    filename = join(directory, date.today().isoformat() + '_' + filepostfix + '.json')
#    with open(filename,'a') as f:
#        f.write(data)
#    return True

#ondata_handler = jsonfile_ondata_handler
pathRoot = '/gws/projects/project-tweetpdsentiment/workspace/share'

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

