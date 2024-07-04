import backtrader

class RSI(backtrader.Strategy):
    params = (('period', 14),)
    
    def log(self, txt, dt=None):
        '''Logging Function'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.rsi = backtrader.indicators.RelativeStrengthIndex(self.data, period=self.params.period)
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        if order.status == order.Completed:
            if order.isbuy():
                self.log("BUY EXECUTED, Price: {}".format(order.executed.price))
            elif order.issell():
                self.log("SELL EXECUTED, Price: {}".format(order.executed.price))
        
        self.order = None
        
    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        
        #Prevents buying/selling stock if there is an order being made
        if self.order:
            return
        
        if self.rsi < 30 and not self.position:
            self.log('BUY CREATED, %.2f' % self.dataclose[0])
            self.order = self.buy()
        elif self.rsi > 70 and self.position:
            self.log("SELL CREATED, %.2f" % self.dataclose[0])
            self.order = self.sell()