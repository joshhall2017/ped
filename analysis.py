from datetime import datetime
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd
import requests
import json


def str_to_datetime(date_str):
    """
    Convert a string to a datetime object
    """
    return datetime.strptime(date_str, '%d/%M/%Y')

def get_num_games(text):
    """
    Clean suspension data and return an integer
    """

    res = text.replace(' games', '')
    res = res.replace(' days', '')
    res = res.replace('^', '')
    res = res.replace(' 2013,2014 season', '')
    res = res.replace('2014 season ', '')
    res = res.replace('Lifetime Ban', '200')
    res = res.replace('Season', '')
    res = res.replace('[A]', '')
    res = res.replace('[B]', '')
    res = res.replace('(', '')
    res = res.replace(')', '')
    res = int(res)

    return res

def get_year(date_obj):
    return date_obj.year

def get_city(text):
    team = text.split()
    team.pop()
    if 'Angels of Anaheim' in text:
        team.pop()
        team.pop()
    if 'Blue Jays' in text:
        team.pop()
    if "White Sox" in text:
        team.pop()
    team = ' '.join(team)
    return team


def get_lat_long(cityName):
    """
    Use the geonames api to grab the latitude and longitude from a cityName
    """
    url = 'http://api.geonames.org/searchJSON'
    data = {'q': cityName, 'maxRows': 1, 'username': 'joshhall2017'}

    res = requests.get(url, params=data)
    data = json.loads(res.text)
    lat = data['geonames'][0]['lat']
    lng = data['geonames'][0]['lng']

    return [lat, lng]

def lin_reg(data):
    res = sm.OLS(data['penalty'],sm.add_constant(data['date_int'])).fit() #y-data first
    print(res.summary())


def plots(data):
    data.plot.scatter(x='date_year', y='penalty',s=None,c=None)
    data.hist(column='penalty')
    plt.show()

data = pd.read_csv('ped.csv') #pandas dataframe
data['Date'] = data['Date'].apply(str_to_datetime) #convert all the dates to objects
data = data.rename(columns = {'penatly' : 'penalty'}) #typo in csv
data['penalty'] = data['penalty'].apply(get_num_games) #convert all the penaltys to numbers

data['date_int'] = data.Date.astype(np.int64)/(10**18)
data['date_year'] = data.Date.apply(get_year) #make a column of all the years\
data['city'] = data.Team.apply(get_city)
data.to_csv('clean_data.csv',sep=',')

#lin_reg(data)
#plots(data)

city_counts = {}
for city in data['city']:
    if city in city_counts:
        city_counts[city] = city_counts[city] + 1
    else:
        city_counts[city] = 1
    #print(city, get_lat_long(city))
print(city_counts)

city_coords = {}
for city in city_counts:
    city_coords[city] = get_lat_long(city)
print(city_coords)


themap = Basemap(projection='gall',
              llcrnrlon = -180,              # lower-left corner longitude
              llcrnrlat = 0,               # lower-left corner latitude
              urcrnrlon = -10,               # upper-right corner longitude
              urcrnrlat = 83,               # upper-right corner latitude
              resolution = 'l',
              area_thresh = 100000.0,
              )
themap.drawcoastlines()
themap.fillcontinents(color = 'green')
themap.drawmapboundary(fill_color='steelblue')
smallest = 100
next_smallest = 100
for city in city_counts:
    lat, long = city_coords[city]
    lat, long = float(lat), float(long)
    if smallest > lat:
        next_smallest = smallest
        smallest = lat
    x, y = themap(long, lat)
    themap.plot(x, y, 'o', color='red', markersize=city_counts[city])
print(smallest, next_smallest)
plt.show()
# 32.010325, -123.916128 # Bottom left
# 47.415015, -66.869620  # Top right
