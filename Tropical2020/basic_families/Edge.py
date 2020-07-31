from typing import Set

from .Vertex import Vertex


class Edge(object):
    # name_ should be a string identifier - only unique if the user is careful (or lucky) to make it so
    # length_ should be a monoid element
    # vert1_ should be a vertex
    # vert2_ should be a vertex
    def __init__(self, name_: str, length_, vert1_: Vertex, vert2_: Vertex) -> None:
        self.name: str = name_
        self._length = length_

        # Distinguished endpoints to help identify self loops, and for other purposes
        self.vert1: Vertex = vert1_
        self.vert2: Vertex = vert2_

    @property
    def length(self):
        return self._length

    # Control how the length property is set
    # length_ should be a monoid element
    @length.setter
    def length(self, length_) -> None:
        self._length = length_

    # The set of vertices is a read only property computed upon access
    @property
    def vertices(self) -> Set[Vertex]:
        return {self.vert1, self.vert2}
