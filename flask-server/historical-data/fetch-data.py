import yfinance

sp500_data = yfinance.download('PFE', start='2000-01-01', end='2024-01-01')
sp500_data.to_csv('PFE.csv')