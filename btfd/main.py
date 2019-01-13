import backtrader as bt
from btfd import util,myclasses,batch, download

inizio = 0
fine = 1249
exchanges = ['Bittrex', 'Cryptopia','YoBit','CoinExchange']
workers = 5

#download.coin_list(inizio,fine)    #estremi esclusi
coins = ['RKC']

batch.infos(coins,workers)
print(download.chart(coins[0]))
#batch.tweets(coins,workers) #twitter sembra tagliare la connessione con 5 workers mmh

for coin in coins:          #TODO: async
    if util.get_exchange(coin) in exchanges:
        #util.merge_csv(coin)
        data = myclasses.OHLCT(dataname='./data/' + coin + '/price.csv')

        class ImDumb(bt.Strategy):
            def __init__(self):
                self.tmf = myclasses.TwiggsMoneyFlow()
                #self.tsf = myclasses.TweetsShitpostFlow()

        cerebro = bt.Cerebro()
        cerebro.addstrategy(ImDumb)
        cerebro.adddata(data)
        cerebro.addsizer(bt.sizers.PercentSizer, percents=99.8)
        cerebro.broker.set_cash(300)
        cerebro.broker.setcommission(commission=0.002)
        cerebro.run()
        cerebro.plot()
        print(coin + ' profit: ' + str(cerebro.broker.getvalue() - 300))


