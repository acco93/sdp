class TNode:

    def __init__(self, name: str):
        self.name = name
        self.outgoing = set()
        self.incoming = set()

    def __repr__(self):
        return f"'{self.name}'"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.name == other.name

    def add_outgoing(self, other):
        self.outgoing.add(other)

    def add_incoming(self, other):
        self.incoming.add(other)
