from datetime import datetime
import matplotlib.pyplot as plt
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



data = pd.read_csv('ped.csv') #pandas dataframe
data['Date'] = data['Date'].apply(str_to_datetime) #convert all the dates to objects
data = data.rename(columns = {'penatly' : 'penalty'}) #typo in csv
data['penalty'] = data['penalty'].apply(get_num_games) #convert all the penaltys to numbers

data.plot.scatter(x='Date', y='penalty',s=None,c=None)

data.hist(column='penalty')
plt.show()
