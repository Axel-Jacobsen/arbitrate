import exchange_basics
import ccxt
import graph_tool.all as gt
import time

"""
Script to graph the json data that we eff with
"""

quadrigacx = ccxt.quadrigacx()
binance    = ccxt.binance()

vertex_name_map = {}

g = gt.Graph()
v_label = g.new_vertex_property('string')
e_label = g.new_edge_property('string')

conversion_set = exchange_basics.analyze_raw_tickers(exchange_basics.get_tickers(binance))
# `conversion` example: ('BTC/ETH', 2.718) - index 0 is the currencies, index 1 is the conversion
t1 = time.time()
for conversion in conversion_set:
    currencies = conversion[0].split('/')

    ## Could probably DRY it up here and not have the exact same code for 
    ## currencies[0] and currencies[1]
    if currencies[0] not in vertex_name_map.keys():
        # Create the new vertex
        v_from = g.add_vertex()
        # Add the vertex to the reference map (i.e. vertex_name_map)
        vertex_name_map[currencies[0]] = g.vertex_index[v_from]
        # Add label to vertex properties
        v_label[v_from] = currencies[0]
    else:
        # If this is not a new currency, just grab the vertex from the graph
        v_from = g.vertex(vertex_name_map[currencies[0]])

    if currencies[1] not in vertex_name_map.keys():
        # Create the new vertex
        v_to = g.add_vertex()
        # Add the vertex to the reference map (i.e. vertex_name_map)
        vertex_name_map[currencies[1]] = g.vertex_index[v_to]
        # Add label to vertex properties
        v_label[v_to] = currencies[1]
    else:
        # If this is not a new currency, just grab the vertex from the graph
        v_to = g.vertex(vertex_name_map[currencies[1]])

    # Add the new edge between v_from to v_to, and label it with the conversion
    new_edge = g.add_edge(v_from, v_to)
    e_label[new_edge] = str(conversion[1])

t2 = time.time()

print('{:.2} seconds to parse data into graph with {} verticies and {} edges'.format(t2 - t1, len(list(g.vertices())), len(list(g.edges()))))

g.vertex_properties['labels'] = v_label
g.edge_properties['labels'] = e_label
g.save('graph.xml')

# pos = gt.sfdp_layout(g, C=5, K=10)
# gt.graph_draw(g,  pos=pos, vertex_text=v_label, edge_text=e_label, output_size=(1000, 1000))
state = gt.minimize_nested_blockmodel_dl(g, deg_corr=True)
gt.draw_hierarchy(state, vertex_text=v_label, edge_text=e_label)
