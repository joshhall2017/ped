from datetime import datetime
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd



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
    print(team)


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


themap = Basemap(projection='gall',
              llcrnrlon = -15,              # lower-left corner longitude
              llcrnrlat = 28,               # lower-left corner latitude
              urcrnrlon = 45,               # upper-right corner longitude
              urcrnrlat = 73,               # upper-right corner latitude
              resolution = 'l',
              area_thresh = 100000.0,
              )

themap.drawcoastlines()
themap.drawcountries()
themap.fillcontinents(color = 'gainsboro')
themap.drawmapboundary(fill_color='steelblue')
themap.plot(5, 5,
            'o',                    # marker shape
            color='Indigo',         # marker colour
            markersize=4            # marker size
            )
plt.show()
