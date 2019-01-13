import backtrader as bt
import btfd.util as util

class TweetsShitpostFlow(bt.Indicator):
    lines = ('tsf',)
    params = (('period', 0),)

    def next(self):
        self.lines.tsf[0] = self.data.tweet[0]

class TwiggsMoneyFlow(bt.Indicator):
    lines = ('tmf',)
    params = (('period', 24*4*21),)
    trh, trl, ad, vol = 0, 0, 0, 0

    def __init__(self):
        self.addminperiod(self.p.period)

    def next(self):
        i = self.p.period
        trh, trl, ad, vol = 0, 0, 0, 0
        while i > 0:
            trh = max(self.data.high[0-i], self.data.close[-1-i])
            trl = min(self.data.low[0-i], self.data.close[-1-i])
            tr = trh - trl
            if tr == 0:
                tr = 999999
            ad = ad + ((((self.data.close[0-i] - trl) - (trh - self.data.close[0-i]))/tr) * self.data.volume[0-i])
            vol = vol + self.data.volume[0-i]
            i = i - 1

        trh = max(self.data.high[0], self.data.close[-1])
        trl = min(self.data.low[0], self.data.close[-1])
        tr = trh - trl
        if tr == 0:
            tr = 999999
        ad = (ad * (self.p.period-1 / self.p.period)) + ((((self.data.close[0] - trl) - (trh - self.data.close[0]))/tr) * self.data.volume[0])
        vol = (vol * (self.p.period-1 / self.p.period)) + self.data.volume[0]

        if vol == 0:
            self.lines.tmf[0] = 0
        else:
            self.lines.tmf[0] = ad / vol

class OHLCT(bt.feeds.GenericCSVData):
    lines = ('tweet',)

    params = (
        ('nullvalue', 0.0),
        ('dtformat', '%Y-%m-%d %H:%M:%S'),
        ('datetime', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('openinterest', -1),
        ('tweet', -1)
    )
