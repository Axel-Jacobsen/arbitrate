import exchange_basics
import ccxt
import json

"""
Script to prepare the json data that we eff with
"""

quadrigacx = ccxt.quadrigacx()
binance = ccxt.binance()

g = {
    'nodes': [],
    'links': []
}
node_set = set()

conversion_set = exchange_basics.analyze_raw_tickers(
    exchange_basics.get_tickers(binance)
)

for conversion in conversion_set:
    currencies = conversion[0].split('/')

    if currencies[0] not in node_set:
        g['nodes'].append({'id': currencies[0]})
        node_set.add(currencies[0])

    if currencies[1] not in node_set:
        g['nodes'].append({'id': currencies[1]})
        node_set.add(currencies[1])

    g['links'].append(
        {'source': currencies[0], 'target': currencies[1], 'value': conversion[1]}
    )

with open('graph.json', 'w') as f:
    json.dump(g, f)
