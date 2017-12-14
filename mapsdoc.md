# maps.py Doc

I've uploaded the maps.py file to github which is the script that produces the map of tweets in california and a normalized version of that plot. There are several files you'll need in order for the script to run. The script also saves the files to my data folder under my username so you may need to change these locations.

maps.py grabs tweets from the previous day and makes maps that describe where the most tweets are coming from within California.

<b> function get_data </b>: grabs the json file and stores it

<b> function make_gdf </b>: grabs select values from the json files and makes a geodataframe

<b> function join_dfs </b>: joins a the map file with the geodataframe from get_data



