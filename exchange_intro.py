import ccxt
import json

quadrigacx   = ccxt.quadrigacx()

with open('quote.json', 'w') as f:
    json.dump(quadrigacx.fetch_ticker('BTC/CAD'), f)
    
  