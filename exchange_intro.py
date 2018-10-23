import ccxt
import json

quadrigacx = ccxt.quadrigacx()
vaultoro   = ccxt.vaultoro()

with open('quote.json', 'w') as f:
    # json.dump(quadrigacx.fetch_ticker('BTC/CAD'), f)
    json.dump(vaultoro.fetch_ticker('BTC/USD'), f)
    

def get_spread(exchange, ticker):
    orderbook = exchange.fetch_order_book(ticker)
    bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
    spread = (ask - bid) if (bid and ask) else None
    return (exchange.id, 'market price', { 'bid':  bid, 'ask': ask, 'spread': spread })

print(get_spread(quadrigacx, 'BTC/CAD'))
print(get_spread(vaultoro, 'BTC/USD'))
