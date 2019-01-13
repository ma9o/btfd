import concurrent.futures
import asyncio
import pandas as pd
from btfd import download,util

def charts(coins,workers):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(charts_wrapper(coins,workers))

async def charts_wrapper(coins,workers):

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        loop = asyncio.get_event_loop()
        futures=[loop.run_in_executor(executor,download.chart,x) for x in coins]
        for response in await asyncio.gather(*futures):
            print(response)

def infos(coins,workers):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(infos_wrapper(coins,workers))

async def infos_wrapper(coins,workers):
    res = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        loop = asyncio.get_event_loop()
        futures=[loop.run_in_executor(executor,download.coin_info,x) for x in coins]
        for response in await asyncio.gather(*futures):
            res.append(response)
    df = pd.DataFrame(res)
    df.columns = ['coin','exchange','percent']
    df.to_csv('./data/info.csv',header=False,index=False)

def tweets(coins,workers):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tweets_wrapper(coins,workers))

async def tweets_wrapper(coins,workers):

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        loop = asyncio.get_event_loop()
        futures=[loop.run_in_executor(executor,download.tweets,x,10) for x in coins]
        for response in await asyncio.gather(*futures):
            print(response)

