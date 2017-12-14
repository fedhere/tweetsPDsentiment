import pandas as pd
import datetime as dt
import json
import os
import geopandas as gpd
import pylab as pl
from geopandas import GeoDataFrame as gdf
from shapely.geometry import Point
import locale
import numpy as np

def get_data(file):
    user_jsons = []
    with open("/gpfs1/cusp/pa1303/betagov/data/" + file, 'r') as f:
        for line in f:
            while True:
                try:
                    jfile = json.loads(line)
                    break
                except ValueError:
                    # Not yet a complete JSON value
                    line += next(f)
            user_jsons.append(jfile)
    return user_jsons

def make_gdf(jsons):
    longs = []
    lats = []
    name = []
    tweets = []
    for i in range(len(jsons)):
        if jsons[i]["coordinates"] is not None:
            longs.append(jsons[i]["coordinates"]["coordinates"][0])
            lats.append(jsons[i]["coordinates"]["coordinates"][1])
            tweets.append(jsons[i]['text'])
            name.append(jsons[i]["user"]["screen_name"])
            
    myDict = {"longs": longs, "lats": lats, "name":name}
    df = pd.DataFrame(myDict)
    geometry = [Point(xy) for xy in zip(df.longs, df.lats)]
    df = df.drop(['longs', 'lats'], axis=1)
    crs = {'init': 'epsg:4326'}
    gdf = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)
    return gdf

def join_dfs(map_file, gdf):
    base = gpd.read_file(map_file)
    gdf = gdf.to_crs(base.crs)
    joined = gpd.sjoin(base, gdf, op='intersects', how='inner')
    counts = joined.groupby('NAME').size()
    counts = counts.to_dict()
    base['counts'] = base['NAME'].apply(lambda x:counts[x] if x in counts.keys() else 0)
    base['counts2'] = base['counts'] / sum(base['counts'])
    base['logcounts'] = np.log10(base['counts']+1) 
    return base

date = dt.date.today() - dt.timedelta(days=1)
data = get_data(str(date) + '_Police_tweets.json')
cali_tweets = make_gdf(data)
cali_joined = join_dfs('/gpfs1/cusp/pa1303/betagov/data/ca_counties/CA_Cities_TIGER2016.shp', cali_tweets)

cali_pop = pd.read_csv('/gpfs1/cusp/pa1303/betagov/data/county_pop.csv')
cali_pop = cali_pop[['State/County', 'Pop_2017']]
cali_with_pop = cali_joined.merge(cali_pop, left_on='NAME', right_on='State/County')
base = gpd.read_file("/gpfs1/cusp/pa1303/betagov/data/ca_tract/cb_2016_06_tract_500k.shp")
base = base[base.COUNTYFP == '071']
cali_tweets = cali_tweets.to_crs(base.crs)
joined = gpd.sjoin(base, cali_tweets, op='intersects', how='inner')
counts = joined.groupby('TRACTCE').size()
counts = counts.to_dict()
base['counts'] = base['TRACTCE'].apply(lambda x:counts[x] if x in counts.keys() else 0)

base['counts'] = base['counts'] / sum(base['counts'])
base['logcounts'] = np.log10(base['counts']+1) 
base = base.to_crs(epsg=3857)
frames = [cali_joined, base]
cali_joined = pd.concat(frames)
cali_joined = cali_joined[cali_joined.NAME != 'San Bernardino']

newpath = r'/gpfs1/cusp/pa1303/betagov/data/' + str(date) + 'map_plots' 
if not os.path.exists(newpath):
    os.makedirs(newpath)
fig = pl.figure(figsize=(8, 18))
ax = fig.add_subplot(111)

cali_joined[cali_joined.counts > 0].plot(column='counts',cmap='OrRd', edgecolor='black',ax=ax, scheme='quantiles', legend=True)

pl.savefig(newpath+'/calipop.pdf')

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
cali_with_pop['Pop_2017'] = cali_with_pop['Pop_2017'].apply(locale.atoi)
cali_with_pop['tweets_normed'] = cali_with_pop['counts'] / cali_with_pop['Pop_2017']

fig = pl.figure(figsize=(8, 18))
ax = fig.add_subplot(111)

cali_with_pop[cali_with_pop.counts > 0].plot(ax=ax, column='tweets_normed', cmap='OrRd', edgecolor='black', legend=True)

pl.savefig(newpath+'/cali_norm_pop.pdf')
