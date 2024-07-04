import backtrader as bt
from datetime import datetime

class MeanReversionStrategy(bt.Strategy):
    params = (
        ('period', 20),          
        ('devfactor', 2),        
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.bar_executed = 0
        
        self.sma = bt.indicators.SimpleMovingAverage(self.dataclose, period=self.params.period)
        self.stdev = bt.indicators.StandardDeviation(self.dataclose, period=self.params.period)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            elif order.issell():
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        if self.order:
            return

        mean = self.sma[0]
        std_dev = self.stdev[0]
        price = self.dataclose[0]

        self.log(f'Close: {price:.2f}, Mean: {mean:.2f}, StdDev: {std_dev:.2f}')

        if price < (mean - self.params.devfactor * std_dev):
            if not self.position:  # Only buy if not already in a position
                self.order = self.buy()
                self.log(f'BUY CREATE, Price: {price:.2f}')
        
        elif price > (mean + self.params.devfactor * std_dev):
            if self.position:  # Only sell if currently in a position
                self.order = self.sell()
                self.log(f'SELL CREATE, Price: {price:.2f}')