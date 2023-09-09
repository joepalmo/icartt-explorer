import pandas as pd
import numpy as np
from datetime import datetime

def read_data_ict(file, tscols=["UTC", "UTC_mid", "Time_Start", "UTC_Start"], delim_whitespace=False, ):
    lineStart = pd.read_csv(file, nrows = 1, header=None, delim_whitespace=delim_whitespace, encoding='latin1')[0][0] - 1
    file.seek(0)
    data = pd.read_csv(file, skiprows = lineStart, delim_whitespace=delim_whitespace, encoding='latin1')
    file.seek(0)
    # get fillValue
    fillValue = pd.read_csv(file, skiprows = 11, nrows = 1, header = None, delim_whitespace=delim_whitespace, encoding='latin1')[0][0]
    file.seek(0)
    # replace fillValue with NA
    data[data == fillValue] = np.nan
    
    # read in date of flight
    read_date = pd.read_csv(file, skiprows = 6, nrows = 1, header = None, delim_whitespace=delim_whitespace, encoding='latin1')
    date_info = [read_date[0][0],read_date[1][0],read_date[2][0]]
    flight_date = '-'.join([str(n) for n in date_info])
    
    # update timestamp to datetime -> timestamp is seconds from beginning of day
    time_col_name = list(set(tscols).intersection(data.columns.to_list()))[0]
    data["timestamp"] = pd.to_datetime(data[time_col_name], unit='s', origin=pd.Timestamp(flight_date))
    
    data.set_index("timestamp", drop=True, inplace=True)
    data.sort_index(inplace=True)

    #get lat long columns
    for x in data.columns.to_list():
        if 'latitude' in x.lower():
            data.rename(columns={x:"latitude"}, inplace=True)
            break
        elif ('_lat' in x.lower()):
            data.rename(columns={x:"latitude"}, inplace=True)
            break

    for x in data.columns.to_list():
        if 'longitude' in x.lower():
            data.rename(columns={x:"longitude"}, inplace=True)
            break
        elif ('_lon' in x.lower()):
            data.rename(columns={x:"longitude"}, inplace=True)
            break

    return data