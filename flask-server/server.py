from flask import Flask
import backtrader
import datetime 
from strategies import BB, MeanReversionStrategy, MACD, MovingAverageCrossover, RSI
app = Flask(__name__)


#members API route
@app.route("/members")
def members():
    return{"members": ["1", "2", "3"]}

@app.route("/trade")
def trade():
    cerebro = backtrader.Cerebro()

    cerebro.broker.set_cash(1000000)

    data = backtrader.feeds.YahooFinanceCSVData(
        dataname= r"historical_data\SP500_data.csv",
        fromdate = datetime.datetime(2000,1,1),
        todate = datetime.datetime(2024,1,1),
        reverse=False)

    cerebro.adddata(data)
    cerebro.addstrategy(MovingAverageCrossover)
    cerebro.addsizer(backtrader.sizers.FixedSize, stake=500)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()
    return


if __name__ == "__main__":
    app.run(debug=True)