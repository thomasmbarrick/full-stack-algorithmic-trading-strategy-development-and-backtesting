import backtrader



class MACD(backtrader.Strategy):
    params = (
        ('fast_ema_period', 12),
        ('slow_ema_period', 26),
        ('signal_period', 9),
    )
    
    def log(self, txt, dt=None):
        '''Logging function'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.bar_executed = 0
        
        # Add MACD indicator
        self.macd = backtrader.indicators.MACD(
            self.datas[0],
            period_me1=self.params.fast_ema_period,
            period_me2=self.params.slow_ema_period,
            period_signal=self.params.signal_period
        )
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        self.order = None
        
    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        
        if self.order:
            return
        
        if not self.position:
            if self.macd.macd[0] > self.macd.signal[0]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()
        else:
            if self.macd.macd[0] < self.macd.signal[0]:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()