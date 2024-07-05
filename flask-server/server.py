from flask import Flask
import backtrader
import datetime 
from strategies import BB, MeanReversionStrategy, MACD, MovingAverageCrossover, RSI
app = Flask(__name__)
import json 
import os
import pathlib
#members API route
@app.route("/companies")
def companies():
    historical_data_path = os.path.join(os.getcwd(), "flask-server", "historical_data.json")
    print(f"this is the historical data path {historical_data_path}")
    f = open(historical_data_path)
    data = json.load(f)
    return data
 


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