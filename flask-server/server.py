from flask import Flask, request, jsonify
import backtrader
import datetime
from strategies import BB, MeanReversionStrategy, MACD, MovingAverageCrossover, RSI
import json
import os

app = Flask(__name__)

"""
TODO - MMMVP
*   - Dropdown for selected stock
*   - Allow users to set sizer
*   - Allow users to set cash
*   - Allow users to set timeframe
*   - Update return API route so it works for all dropdown menus
*   - Trade API route hookup selected strategy and stock
*   - Graphing
"""

"""Opening necessary JSON documents"""
historical_data_path = os.path.join(os.getcwd(), "flask-server", "historical_data.json")
with open(historical_data_path, "r") as historical_data_file:
    historical_data = json.load(historical_data_file)
    
strategy_path = os.path.join(os.getcwd(), "flask-server", "strategy.json")
with open(strategy_path, "r") as strategy_file:
    strategy = json.load(strategy_file)

#! Needs to always be set to "ticker" and "class_title" as that is what is needed - ensure the case when updated from front end
selected_stock = historical_data["Companies"][0]['ticker']
selected_strategy = strategy["Strategies"][0]["class_title"]

stake = 500
broker_cash = 1000000

"""API route to get companies from historical_data json"""
@app.route("/companies")
def companies():
    return jsonify(historical_data)

""" API route to return selected Stock to front end"""
@app.route("/selectedStock")
def selected_stock_route():
    global selected_stock
    return jsonify({"selectedStock": selected_stock})

""" API route to return selected strategy to front end"""
@app.route("/selectedStrategy")
def selected_strategy_route():
    global selected_strategy
    return jsonify({"selectedStrategy": selected_strategy})

"""API route to fetch selected stock from the front end/ update """
@app.route("/submit", methods=["POST"])
def submit_selection():
    global selected_stock
    data = request.json
    if data is None:
        return jsonify({"error": "Invalid JSON data"}), 400
    selected_stock = data.get('selectedCompany')
    print(f"Selected company ticker: {selected_stock}")
    return jsonify({"message": "Selection received", "selectedCompany": selected_stock})

@app.route("/submitStrategy", methods=["POST"])
def submit_strategy():
    global selected_strategy
    data = request.json
    if data is None:
        return jsonify({"error": "Invalid JSON data"}), 400
    selected_strategy = data.get('selectedStrategy')
    print(f"Selected strategy: {selected_strategy}")
    return jsonify({"message": "Selection received", "selectedStrategy": selected_strategy})

@app.route("/setParameters", methods=["POST"])
def set_parameters():
    global stake, broker_cash
    data = request.json
    if data is None:
        return jsonify({"error": "Invalid JSON data"}), 400
    stake = data.get('stake', stake)
    broker_cash = data.get('brokerCash', broker_cash)
    print(f"Stake: {stake}, Broker Cash: {broker_cash}")
    return jsonify({"message": "Parameters updated", "stake": stake, "brokerCash": broker_cash})

"""API route to get strategies from strategies JSON"""
@app.route("/strategies")
def strategies():
    return jsonify(strategy)

"""API route to get strategy description"""
@app.route("/strategyDescription")
def strategy_description():
    global selected_strategy
    for strat in strategy["Strategies"]:
        if strat["class_title"] == selected_strategy:
            return jsonify({"description": strat["description"]})
    return jsonify({"error": "Strategy not found"}), 404

""" API Route to make trade"""
@app.route("/trade")
def trade():
    cerebro = backtrader.Cerebro()
    cerebro.broker.set_cash(broker_cash)

    data_path = os.path.join("historical_data", f"{selected_stock}.csv")
    data = backtrader.feeds.YahooFinanceCSVData(
        dataname=data_path,
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2024, 1, 1),
        reverse=False)

    cerebro.adddata(data)

    strategy_map = {
        "BB": BB,
        "MeanReversionStrategy": MeanReversionStrategy,
        "MACD": MACD,
        "MovingAverageCrossover": MovingAverageCrossover,
        "RSI": RSI
    }

    cerebro.addstrategy(strategy_map[selected_strategy])
    cerebro.addsizer(backtrader.sizers.FixedSize, stake=stake)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
    return jsonify({"message": "Trade executed"})

if __name__ == "__main__":
    app.run(debug=True)




