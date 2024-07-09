"""
*This is an easy to change script that recieves all the available stock data
*from the beginning of the century to the start of 2024. The data is sourced
*using Yahoo Finance.
"""


import yfinance

data = yfinance.download('DIS', start='2000-01-01', end='2024-01-01')
data.to_csv('DIS.csv')