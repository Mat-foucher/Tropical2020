from .Vertex import Vertex
from typing import Set


class Leg(object):
    # name_ should be a string identifier - only unique if the user is careful (or lucky) to make it so
    # root_ should be a vertex
    def __init__(self, name_: str, root_: Vertex) -> None:
        self.name: str = name_
        self.root: Vertex = root_

    # The set of vertices is a read only property computed upon access
    @property
    def vertices(self) -> Set[Vertex]:
        return {self.root}
