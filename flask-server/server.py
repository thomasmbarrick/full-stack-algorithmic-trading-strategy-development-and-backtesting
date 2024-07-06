from flask import Flask, request, jsonify 
import backtrader
import datetime 
from strategies import BB, MeanReversionStrategy, MACD, MovingAverageCrossover, RSI
import json 
import os
import pathlib

app = Flask(__name__)

historical_data_path = os.path.join(os.getcwd(), "flask-server", "historical_data.json")
with open(historical_data_path, "r") as hisorical_data_file:
    historical_data = json.load(hisorical_data_file)

selected_stock = historical_data["Companies"][0]['ticker']

# API route to get companies
@app.route("/companies")
def companies():
    return jsonify(historical_data)

# API route to get the selected stock
@app.route("/selectedStock")
def selected_stock_route():
    global selected_stock
    return jsonify({"selectedStock": selected_stock})

# API route to submit selection
@app.route("/submit", methods=["POST"])
def submit_selection():
    global selected_stock
    data = request.json
    selected_stock = data.get('selectedCompany')
    print(f"Selected company ticker: {selected_stock}")
    return jsonify({"message": "Selection received", "selectedCompany": selected_stock})

@app.route("/trade")
def trade():
    cerebro = backtrader.Cerebro()
    cerebro.broker.set_cash(1000000)

    data = backtrader.feeds.YahooFinanceCSVData(
        dataname=os.path.join("historical_data", "SP500_data.csv"),
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2024, 1, 1),
        reverse=False)

    cerebro.adddata(data)
    cerebro.addstrategy(MovingAverageCrossover)
    cerebro.addsizer(backtrader.sizers.FixedSize, stake=500)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
    return jsonify({"message": "Trade executed"})

if __name__ == "__main__":
    app.run(debug=True)
