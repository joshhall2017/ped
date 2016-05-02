from datetime import datetime
import pandas as pd



def str_to_datetime(date_str):
    """
    Convert a string to a datetime objec
    """

    return datetime.strptime(date_str, '%d/%M/%Y')



data = pd.read_csv('ped.csv') #pandas dataframe

data['Date'] = data['Date'].apply(str_to_datetime)
print(data)
