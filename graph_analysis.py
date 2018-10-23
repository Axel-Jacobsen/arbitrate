import exchange_basics
import ccxt
from graph_tool.all import *

print('modules loaded')

quadrigacx = ccxt.quadrigacx()
binance    = ccxt.binance()

vertex_name_map = {}

g = Graph()

conversion_set = exchange_basics.analyze_raw_tickers(exchange_basics.get_tickers(binance))
for conversion in conversion_set:
    currencies = conversion[0].split('/')
    if currencies[0] not in vertex_name_map.keys():
        v_from = g.add_vertex()
        vertex_name_map[currencies[0]] = g.vertex_index[v_from]
    else:
        v_from = g.vertex(vertex_name_map[currencies[0]])

    if currencies[1] not in vertex_name_map.keys():
        v_to = g.add_vertex()
        vertex_name_map[currencies[1]] = g.vertex_index[v_to]
    else:
        v_to = g.vertex(vertex_name_map[currencies[1]])

    g.add_edge(v_from, v_to)

print(vertex_name_map)
pos = sfdp_layout(g)
graph_draw(g,  pos=pos)
