import json

from TGraph import TGraph


def parse(path: str):
    raw_json = json.load(open(path))

    graph = TGraph()

    for item in raw_json:

        node_a = item["from"]
        node_b = item["to"]
        bidirectional = item["bidirectional"]

        graph.add_node(node_a)
        graph.add_node(node_b)
        graph.add_arc(node_a, node_b)

        if bidirectional:
            graph.add_arc(node_b, node_a)

    return graph
