import sys

import utils


def main():

    if len(sys.argv) != 2:
        sys.exit(1)

    path = sys.argv[1]

    graph = utils.parse(path)

    graph.plot()

    for node_id in graph.nodes:
        graph.paths_from(node_id)


if __name__ == "__main__":
    main()
