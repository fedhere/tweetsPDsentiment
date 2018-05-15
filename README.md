# tweetsPDsentiment
This code lets users collect streaming tweets related to criminal justice from any location using the tweepy api. 
### Getting Started
In order to collect tweets from the command line inside the dev folder run

    python stream.py <location name>
    
The location name should be city_state. 
Example: cincinnati_oh

This location must also have two configuration files named \<location name\>.cfg and \<location name_gkw\>.cfg
These configuration files contain the tweepy access tokens, keywords, and location details which are needed to collect tweets

Using the scripts it is straightforward to add a new location to collect tweets from.  In the inputs folder you should create a csv file named keys.csv. The headings should be: 

jurisdiction, name, API Key, API Secret, Access token, Access token secret

Jurisdiction is the location of interest. Name is the owner of the API keys. The remaining 4 headings can be retrieved from Twitter when requesting authorization to use the Tweepy API.

Then in the inputs folder add the location to the dictionary juris_dict inside jurisdictions.py. This should include any the coordinates and any specific terms you are interested in.

Running keyword_gen.py that’s inside the dev folder will create the configuration files in the location inputs/placeConfigs. Any number of locations can be called after keyword_gen.py.

Tweets can be collected by running stream.py with the location name. 
### Output
The files will be saved in output/\<location_name\>/tweetStreams.
### Packages Required
Pandas

