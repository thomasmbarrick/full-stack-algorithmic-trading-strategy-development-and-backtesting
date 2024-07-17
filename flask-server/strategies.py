import backtrader as bt
from backtrader.indicators import BollingerBands



class BB(bt.Strategy):
    
    """
    Bollinger Bands Strategy (BB):
    
    This strategy uses Bollinger Bands to generate buy and sell signals. Bollinger Bands consist of a moving average (usually the 20-period moving average)
    and two standard deviation lines plotted above and below the moving average. The strategy buys when the price closes above the upper Bollinger Band and
    sells when it closes below the lower Bollinger Band.

    Parameters:
    - period: Number of periods for calculating the Bollinger Bands (default is 20).
    - stddev: Standard deviation multiplier for the Bollinger Bands (default is 2).
    """
      
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
 
class MeanReversionStrategy(bt.Strategy):
    
    """
    Mean Reversion Strategy:
    
    This strategy is based on the concept that prices tend to revert to their mean over time. It uses the mean (average) price and standard deviation to
    determine buy and sell signals. The strategy buys when the price is significantly below the mean (by a factor of the standard deviation) and sells when
    it is significantly above.

    Parameters:
    - period: Number of periods for calculating the mean and standard deviation (default is 20).
    - devfactor: Factor of standard deviation for determining buy/sell signals (default is 2).
    """   
    
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
  
class MACD(bt.Strategy):
    
    """
    MACD Strategy:
    
    This strategy uses the Moving Average Convergence Divergence (MACD) indicator, which consists of the MACD line, signal line, and histogram.
    The MACD line is the difference between a fast and a slow exponential moving average (EMA). The signal line is an EMA of the MACD line. The 
    strategy buys when the MACD line crosses above the signal line and sells when the MACD line crosses below the signal line.

    Parameters:
    - fast_ema_period: Period for the fast EMA (default is 12).
    - slow_ema_period: Period for the slow EMA (default is 26).
    - signal_period: Period for the signal line (default is 9).
    """
    
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
        self.macd = bt.indicators.MACD(
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
    
class MovingAverageCrossover(bt.Strategy):

    """
    Moving Average Crossover Strategy:
    
    This strategy uses two moving averages (a short-period moving average and a long-period moving average) to generate buy and sell signals. The strategy buys when
    the short-period moving average crosses above the long-period moving average and sells when it crosses below.

    Parameters:
    - short_period: Period for the short moving average (default is 50).
    - long_period: Period for the long moving average (default is 200).
    """

    params = (
        ('short_period', 50),
        ('long_period', 200),  
    )
    
    def log(self, txt, dt=None):
        '''Logging Function'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.short_sma = bt.indicators.SMA(self.data, period=self.p.short_period)
        self.long_sma = bt.indicators.SMA(self.data, period=self.p.long_period)
        
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
        
        
        if self.short_sma > self.long_sma and not self.position:
            self.log('BUY CREATED, %.2f' % self.dataclose[0])
            self.order = self.buy()
        elif self.short_sma < self.long_sma and self.position:
            self.log("SELL CREATED, %.2f" % self.dataclose[0])
            self.order = self.sell()

class RSI(bt.Strategy):
    
    """
    RSI Strategy:
    
    This strategy uses the Relative Strength Index (RSI) to generate buy and sell signals. RSI is a momentum oscillator that measures the speed and change
    of price movements. It oscillates between 0 and 100 and is typically used to identify overbought or oversold conditions in a market. The strategy buys
    when the RSI is below 30, indicating that the asset is oversold and may be undervalued, and sells when the RSI is above 70, indicating that the asset is 
    overbought and may be overvalued.

    Parameters:
    - period: Number of periods for calculating the RSI (default is 14).
    """
    
    params = (('period', 14),)
    
    def log(self, txt, dt=None):
        '''Logging Function'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.rsi = bt.indicators.RelativeStrengthIndex(self.data, period=self.params.period)
        
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