class TNode:

    def __init__(self, name: str):
        self.name = name
        self.outgoing = set()
        self.runtime_parents = set()

    def __repr__(self):
        return f"'{self.name}'"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.name == other.name

    def add_outgoing(self, other):
        self.outgoing.add(other)

    def add_runtime_parent(self, other):
        self.runtime_parents.add(other)

    def clear_runtime_parents(self):
        self.runtime_parents.clear()