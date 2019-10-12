import queue

import networkx as nx

from TNode import TNode
import matplotlib.pyplot as plt


class TGraph:

    def __init__(self):
        self.nodes = {}

    def add_node(self, node_id: str):

        if node_id in self.nodes:
            return

        node = TNode(node_id)
        self.nodes[node_id] = node

    def add_arc(self, node_id0: str, node_id1: str):

        if node_id0 not in self.nodes:
            raise Exception("Error: " + node_id0 + " is not a node")

        if node_id1 not in self.nodes:
            raise Exception("Error: " + node_id1 + " is not a node")

        node0 = self.nodes[node_id0]
        node1 = self.nodes[node_id1]

        node0.add_outgoing(node1)
        node1.add_incoming(node0)

    def plot(self):

        graph = nx.DiGraph()

        for node_id in self.nodes:
            graph.add_node(node_id)

        for node_id in self.nodes:
            node = self.nodes[node_id]
            for outgoing in node.outgoing:
                graph.add_edge(node_id, outgoing.name)

        nx.draw_networkx(graph, pos=nx.kamada_kawai_layout(graph), with_labels=True, arrows=True)
        plt.show()

    def paths_from(self, node_id):

        if node_id not in self.nodes:
            raise Exception("Error: " + node_id + " is not a node")

        print("Checking paths from node '" + node_id + "'")

        root = self.nodes[node_id]

        queued_nodes = queue.Queue()
        queued_nodes.put(root)

        explored = set()
        previous = set()

        while not queued_nodes.empty():

            node = queued_nodes.get()

            if node in explored:
                self.__print_paths(node, root)
            else:
                explored.add(node)
                for outgoing in node.outgoing - previous:
                    queued_nodes.put(outgoing)

            previous.clear()
            previous.add(node)

    def __print_paths(self, node, root):

        print("Node " + str(node) + " is reachable from more than one path:")

        previous = set()

        def __recursive_print_paths(node, root, previous):

            if node == root:
                print(node)
                return
            else:
                print(str(node) + " <- ", end="")

            for incoming in node.incoming.difference(previous):
                singleton = set()
                singleton.add(node)
                __recursive_print_paths(incoming, root, singleton)

        for incoming in node.incoming.difference(previous):
            print("\t" + str(node) + " <- ", end="")
            singleton = set()
            singleton.add(node)
            __recursive_print_paths(incoming, root, singleton)
