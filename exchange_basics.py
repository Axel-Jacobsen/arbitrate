import ccxt
import json

def save_json(json_data, filename):
	with open(filename, 'w') as f:
		json.dump(json_data, f)

def get_spread(exchange, ticker):
	orderbook = exchange.fetch_order_book(ticker)
	bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
	ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
	spread = (ask - bid) if (bid and ask) else None
	return (exchange.id, 'market price', { 'bid':  bid, 'ask': ask, 'spread': spread })

def get_tickers(exchange):
	return exchange.fetch_tickers()

def analyze_raw_tickers(json_data):
	ticker_list = set()
	for ticker in json_data:
		ticker_list.add((ticker, json_data[ticker]['bid']))
	return ticker_list

if __name__ == '__main__':
	quadrigacx = ccxt.quadrigacx()
	binance    = ccxt.binance()
	
	save_json(quadrigacx.fetch_ticker('BTC/CAD'), 'miscellaneous_data/btccad.json')
	save_json(get_tickers(quadrigacx), 'ticker_data/quadrigacx_tickers.json')
	save_json(get_tickers(binance), 'ticker_data/binance_tickers.json')
	analyze_raw_tickers(get_tickers(quadrigacx))
	analyze_raw_tickers(get_tickers(binance))
