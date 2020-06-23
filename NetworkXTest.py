import networkx as nx 
import matplotlib.pyplot as plt
from CombinatorialCurve import *
from Display import *
from RPC import *

'''
G = nx.Graph()

G.add_nodes_from([1,2])
G.add_edge(1,2)

nx.draw(G, with_labels=True, font_weight='bold')
plt.show()
'''

# Set up a free monoid for sake of convenience
freeMonoid = Monoid()
freeMonoid.addgen("a")
freeElementA = freeMonoid.Element({"a": 1})
freeMonoid.addgen("b")
freeElementB = freeMonoid.Element({"b": 1})
freeMonoid.addgen("c")
freeElementC = freeMonoid.Element({"c": 1})
freeMonoid.addgen("d")
freeElementD = freeMonoid.Element({"d": 1})
freeMonoid.addgen("e")
freeElementE = freeMonoid.Element({"e": 1})
freeMonoid.addgen("f")
freeElementF = freeMonoid.Element({"f": 1})
freeMonoid.addgen("g")
freeElementG = freeMonoid.Element({"g": 1})
freeMonoid.addgen("h")
freeElementH = freeMonoid.Element({"h": 1})

C = CombCurve("Example 3.5")

v1 = vertex("v1", 0)
v2 = vertex("v2", 0)
v3 = vertex("v3", 1)
# Take all edges to be of the same length (for sake of mesa testing)
e1 = edge("e1", freeElementA, v1, v2)
e2 = edge("e2", freeElementA, v2, v3)
e3 = edge("e3", freeElementA, v1, v3)
e4 = edge("e4", freeElementA, v1, v1)
l = leg("l", v1)

C.addEdges({e1, e2, e3, e4})
C.addLeg(l)

displayCurve = DisplayCurve(C)
#displayCurve.display("Example3Point5.png")

C = CombCurve("Chain of 9 vertices")
v1 = vertex("v1", 0)
v2 = vertex("v2", 0)
v3 = vertex("v3", 0)
v4 = vertex("v4", 0)
v5 = vertex("v5", 0)
v6 = vertex("v6", 0)
v7 = vertex("v7", 0)
v8 = vertex("v8", 0)
v9 = vertex("v9", 0)
e1 = edge("e1", freeElementA, v1, v2)
e2 = edge("e2", freeElementA, v2, v3)
e3 = edge("e3", freeElementA, v3, v4)
e4 = edge("e4", freeElementA, v4, v5)
e5 = edge("e5", freeElementA, v5, v6)
e6 = edge("e6", freeElementA, v6, v7)
e7 = edge("e7", freeElementA, v7, v8)
e8 = edge("e8", freeElementA, v8, v9)

C.addEdges({e1, e2, e3, e4, e5, e6, e7, e8})
C.monoid = freeMonoid

display2 = DisplayCurve(C)
#display2.display("Chain of 9 Vertices.png")
