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

    def plot(self):

        graph = nx.DiGraph()

        for node_id in self.nodes:
            graph.add_node(node_id)

        for node_id in self.nodes:
            node = self.nodes[node_id]
            for outgoing in node.outgoing:
                graph.add_edge(node_id, outgoing.name)

        pos = nx.kamada_kawai_layout(graph)
        nx.draw_networkx(graph, pos=pos, with_labels=True, arrows=True)
        plt.show()

    def paths_from(self, node_id):

        if node_id not in self.nodes:
            raise Exception("Error: " + node_id + " is not a node")

        print("+++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Checking paths from node '" + node_id + "'")

        for nid in self.nodes:
            self.nodes[nid].clear_runtime_parents()

        root = self.nodes[node_id]

        queued_nodes = queue.Queue()
        queued_nodes.put(root)

        explored = set()

        graph = nx.DiGraph()
        show_graph = False

        while not queued_nodes.empty():

            node = queued_nodes.get()

            graph.add_node(node.name)

            if node in explored:
                self.__print_paths(node, root)
                show_graph = True
            else:
                explored.add(node)
                for outgoing in node.outgoing:

                    graph.add_node(outgoing.name)
                    graph.add_edge(node.name, outgoing.name)

                    if outgoing in node.runtime_parents:
                        continue
                    outgoing.add_runtime_parent(node)
                    queued_nodes.put(outgoing)

        if show_graph:
            nx.draw_networkx(graph, pos=nx.kamada_kawai_layout(graph), with_labels=True, arrows=True)
            plt.show()
        print("+++++++++++++++++++++++++++++++++++++++++++++++++")
        print()

    def __print_paths(self, node, root):

        print()
        print("................................................")
        print("Node " + str(node) + " is reachable from more than one path:")

        previous = set()

        def __recursive_print_paths(node, root, prefix, num):

            print(str(num) + " " + prefix + str(node))

            if node == root:
                return

            for incoming in node.runtime_parents.difference(previous):
                __recursive_print_paths(incoming, root, prefix + "-", num + 1)

        for incoming in node.runtime_parents.difference(previous):
            print()
            print("0 " + str(node))
            __recursive_print_paths(incoming, root, prefix="-", num=1)

        print("................................................")
        print()
