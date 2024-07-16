from flask import Flask, request, jsonify, send_file
import backtrader
import datetime
from strategies import BB, MeanReversionStrategy, MACD, MovingAverageCrossover, RSI
import json
import os
import matplotlib.pyplot as plt

app = Flask(__name__)

# Opening necessary JSON documents
historical_data_path = os.path.join(os.getcwd(), "flask-server/historical_data.json")
with open(historical_data_path, "r") as historical_data_file:
    historical_data = json.load(historical_data_file)

strategy_path = os.path.join(os.getcwd(), "flask-server/strategy.json")
with open(strategy_path, "r") as strategy_file:
    strategy = json.load(strategy_file)

selected_stock = historical_data["Companies"][0]['ticker']
selected_strategy = strategy["Strategies"][0]["class_title"]

stake = 500
broker_cash = 1000000

# API route to get companies from historical_data json
@app.route("/companies")
def companies():
    return jsonify(historical_data)

# API route to return selected Stock to front end
@app.route("/selectedStock")
def selected_stock_route():
    global selected_stock
    return jsonify({"selectedStock": selected_stock})

# API route to return selected strategy to front end
@app.route("/selectedStrategy")
def selected_strategy_route():
    global selected_strategy
    return jsonify({"selectedStrategy": selected_strategy})

# API route to fetch selected stock from the front end/ update
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

# API route to get strategies from strategies JSON
@app.route("/strategies")
def strategies():
    return jsonify(strategy)

# API route to get strategy description
@app.route("/strategyDescription")
def strategy_description():
    global selected_strategy
    for strat in strategy["Strategies"]:
        if strat["class_title"] == selected_strategy:
            return jsonify({"description": strat["description"]})
    return jsonify({"error": "Strategy not found"}), 404

# API route to set parameters (stake and broker cash)
@app.route("/setParameters", methods=["POST"])
def set_parameters():
    global stake, broker_cash
    data = request.json
    if data is None:
        return jsonify({"error": "Invalid JSON data"}), 400
    stake = data.get('stake', stake)
    broker_cash = data.get('brokerCash', broker_cash)
    return jsonify({"message": "Parameters updated", "stake": stake, "brokerCash": broker_cash})

@app.route("/trade")
def trade():
    global selected_stock, selected_strategy, stake, broker_cash
    cerebro = backtrader.Cerebro()
    cerebro.broker.set_cash(broker_cash)
    data_path = os.path.join(os.getcwd(), "flask-server/historical-data", f"{selected_stock}.csv")
    
    # Check if the file exists
    if not os.path.exists(data_path):
        print(f"File not found: {data_path}")
        return jsonify({"error": f"File not found: {data_path}"}), 404

    print(f"Using data from: {data_path}")
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

    if selected_strategy not in strategy_map:
        print(f"Strategy not found: {selected_strategy}")
        return jsonify({"error": f"Strategy not found: {selected_strategy}"}), 404

    cerebro.addstrategy(strategy_map[selected_strategy])
    cerebro.addsizer(backtrader.sizers.FixedSize, stake=stake)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    initial_portfolio_value = cerebro.broker.getvalue()
    cerebro.run()
    final_portfolio_value = cerebro.broker.getvalue()
    print('Final Portfolio Value: %.2f' % final_portfolio_value)

    # Save plot to a file
    fig = cerebro.plot()[0][0]
    plot_path = os.path.join(os.getcwd(), "flask-server", "plot.png")
    fig.savefig(plot_path)
    plt.close(fig)

    result = {
        "initial_portfolio_value": initial_portfolio_value,
        "final_portfolio_value": final_portfolio_value,
        "plot_path": "/plot.png"
    }

    return jsonify(result)

# Endpoint to serve the plot image
@app.route('/plot.png')
def plot_png():
    plot_path = os.path.join(os.getcwd(), "flask-server", "plot.png")
    if os.path.exists(plot_path):
        return send_file(plot_path, mimetype='image/png')
    else:
        return jsonify({"error": "Plot not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)


 