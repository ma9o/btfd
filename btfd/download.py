import requests
import datetime
import os
import time
#from twitterscraper import query_tweets
from bs4 import BeautifulSoup
from btfd import util
import pandas as pd
import re
import ast
from selenium import webdriver

def coin_list(inizio,fine):
    r = requests.get("https://api.coinmarketcap.com/v1/ticker/")
    coins = r.json()
    out = open("./data/coins.csv", "w")
    i = 0
    while i < fine:
        if i > inizio:
            out.write(coins[i]['symbol']+","+coins[i]['id'] + "\n")
        i = i + 1

    out.close()

def coin_info(coin):
    r = requests.get('https://coinmarketcap.com/currencies/' + util.get_id(coin))
    cmc = BeautifulSoup(r.content, 'html.parser')
    exchange = cmc.tbody.contents[1].contents[3].contents[0].string
    percentage = cmc.tbody.contents[1].contents[10].string

    return (coin,exchange,percentage)

def chart(coin):
    exchange = util.get_exchange(coin)
    if not os.path.exists('./data/' + coin): os.makedirs('./data/' + coin)
    try:
        if exchange == 'YoBit':
            r = requests.get("https://yobit.net/en/trade/"+coin+"/BTC")
            id = re.findall("var pair_id = '(.*?)';",r.text)
            r = requests.post("https://yobit.net/ajax/system_chart.php",data={'method':'chart','pair_id':id,'mode':4464})
            chart = r.json()['data']
            for c in chart:
                c[0] = str(datetime.datetime.fromtimestamp(c[0] / 1000.0))[:19]
            df = pd.DataFrame(chart,columns=['time','vol','base','open','high','low','close','0','1','2','3','4','5'])
            del df['base']
            for i in range(6):
                del df[str(i)]
            cols = df.columns.tolist()
            cols = [cols[0]]+cols[2:]+[cols[1]]
            df = df[cols]
            df.to_csv("./data/" + coin + "/price.csv",index=False,header=False)

        if exchange == 'CoinExchange':
            r = requests.get("https://www.coinexchange.io/api/v1/getmarkets")
            for x in r.json()['result']:
                if x['BaseCurrency'] == 'Bitcoin' and x['MarketAssetCode'] == coin:
                    id = x['MarketID']
            driver = webdriver.PhantomJS()
            driver.get("http://www.coinexchange.io/charts/market/data?mid="+id)
            time.sleep(0.3)
            chart = re.findall('wrap;">(.*?)</pre', driver.page_source)
            chart = ast.literal_eval(chart[0])[0]
            for c in chart:
                c[0] = str(datetime.datetime.fromtimestamp(float(c[0])))[:19]
                for i in range(1,6):
                    c[i] = float(c[i])
            df = pd.DataFrame(chart, columns=['time', 'vol', 'open', 'high', 'low', 'close'])
            cols = df.columns.tolist()
            cols = [cols[0]]+cols[2:]+[cols[1]]
            df = df[cols]
            util.list_to_csv(chart, "./data/" + coin + "/price")

        if exchange == 'Cryptopia':
            r = requests.get("https://www.cryptopia.co.nz/api/GetTradePairs")
            for x in r.json()['Data']:
                if x['BaseCurrency'] == 'Bitcoin' and x['Symbol'] == coin:
                    id = str(x['Id'])
            r = requests.get("https://www.cryptopia.co.nz/Exchange/GetTradePairChart?tradePairId="+id+"&dataRange=7&dataGroup=15").json()
            chart = r['Candle']
            volume = r['Volume']
            for c,v in zip(chart,volume):
                c.append(v['y'])
                c[0] = str(datetime.datetime.fromtimestamp(c[0] / 1000.0))[:19]
            util.list_to_csv(chart, "./data/" + coin + "/price")

        if exchange == 'Bittrex':
            r = requests.get("https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=BTC-"+coin+"&tickInterval=oneMin")
            chart = r.json()
            df = pd.DataFrame(chart['result'])
            del df['BV']
            r = 0
            for row in df.itertuples():
                year = int(df.at[r,'T'][:4])
                month = int(df.at[r,'T'][5:7])
                day = int(df.at[r,'T'][8:10])
                hour = int(df.at[r,'T'][11:13])
                min = int(df.at[r,'T'][14:16])
                sec = int(df.at[r,'T'][17:19])
                df.at[r,'T'] = datetime.datetime(year,month,day,hour,min,sec)
                r = r + 1

            cols = df.columns.tolist()
            cols = [cols[4]] + [cols[3]] + [cols[1]] + [cols[2]] + [cols[0]] + [cols[5]]
            df = df[cols]
            df.to_csv('./data/' + coin + '/price.csv', index=False, header=False)

        res = "Succesfully downloaded "+coin+" chart"
    except Exception as e:
        res = "Failed to download "+coin+" chart: "+str(e.with_traceback())

    return res

def tweets(coin, n):
    '''
    Get an histogram  equivalent tuple of the number of tweets for a given coin.
    @param coin: coin name
    @param n: number of tweets to fetch
    '''

    print("Downloading "+coin+" tweets...")
    tweets = []

    for tweet in query_tweets('$' + util.name_to_symbol(coin), n)[:n]:
        tweets.append((tweet.timestamp, int(tweet.likes) + 1))

    tweets.sort(key=lambda x: x[0])

    util.list_to_csv(tweets, "./data/" + coin + "/tweets")