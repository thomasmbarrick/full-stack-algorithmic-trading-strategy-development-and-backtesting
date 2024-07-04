import backtrader as bt
from backtrader.indicators import BollingerBands

class BB(bt.Strategy):
    params = (("period", 20), ("stddev", 2))
    
    def log(self, txt, dt=None):
        '''Logging Function'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.bollinger = BollingerBands(self.datas[0], period=self.params.period, devfactor=self.params.stddev)
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.buyprice = order.executed.price
                self.buycomm = order.executed.value
                self.log("BUY EXECUTED, Price: {}".format(order.executed.price))
                
            if order.issell():
                self.log("SELL EXECUTED, Price: {}".format(order.executed.price))
                
        self.order = None
        
    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        
        if self.dataclose[0] > self.bollinger.lines.top[0] and not self.position:
            self.buy()
        elif self.dataclose[0] < self.bollinger.lines.bot[0] and self.position:
            self.sell()
 