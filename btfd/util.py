import requests
import csv
import math
import pandas as pd

def tmf_div(n, d):
    try:
        res = n / d
    except:
        res = 99999999999999999
    return res

def get_id(coin):
    df = pd.read_csv("./data/coins.csv", names=['symbol','id'])
    return df.loc[df['symbol'] == coin]['id'].values[0]

def list_to_csv(list, name):
    '''
    Convert list to csv 
    :param list: the list to convert
    :param name: csv file path
    '''
    with open(name + ".csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(list)

def get_exchange(coin):
    df = pd.read_csv("./data/info.csv", names=['coin', 'exchange', 'percent'])
    return df.at[df.loc[df['coin'] == coin].index[0], 'exchange']

def merge_csv(coin):
    price = pd.read_csv('./data/' + coin + '/price.csv', names=['time','open','high','low','close','volume'])
    tweets = pd.read_csv('./data/' + coin + '/tweets.csv', names=['time','likes'])
    merged = pd.merge(price, tweets, how='outer', on=['time'])
    merged = merged.sort_values(by='time')
    merged = merged.reset_index(drop=True)
    merged = fill_the_gaps(merged)
    merged.to_csv('./data/' + coin + '/merged.csv',index=False,header=False)

def fill_the_gaps(df):
    n = 0
    stop = False

    for row in df.itertuples():
        if not stop:
            if math.isnan(row[4]):
                n = n + 1
            else:
                stop = True

    df = df.drop(df.head(n).index)
    df = df.reset_index(drop=True)

    r = 1
    for row in df.itertuples():
        if 'previous' not in locals():
            previous = row
        else:
            if math.isnan(row[7]):
                df.at[r,'likes']=0
                previous = row
            else:
                df.at[r, 'open']= previous[2]
                df.at[r, 'high']= previous[3]
                df.at[r, 'low']= previous[4]
                df.at[r, 'close']= previous[5]
                df.at[r, 'volume']= previous[6]
            r = r + 1

    return df




