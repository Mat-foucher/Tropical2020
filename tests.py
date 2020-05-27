from CombinatorialCurve import *
from StrictPiecewiseLinearFunction import *
from ModuliSpaces import *
import time


C = CombCurve("Example 3.5")

v1 = vertex("v1", 0)
v2 = vertex("v2", 0)
v3 = vertex("v3", 1)
e1 = edge("e1", 1.0, v1, v2)
e2 = edge("e2", 1.0, v2, v3)
e3 = edge("e3", 1.0, v1, v3)
e4 = edge("e4", 1.0, v1, v1)
l = leg("l", v1)

C.edges = {e1, e2, e3, e4}
C.legs = {l}

core = C.core

assert core.isConnected
assert core.genus == C.genus


dict = {v1: 1.0, v2: 0.0, v3: 0.0, l: 0.0}

f = StrictPiecewiseLinearFunction(C, dict)



assert f.functionValues[v1] == 1.0
for v in C.vertices:
    assert (f + f).functionValues[v] == f.functionValues[v] + f.functionValues[v]
    assert (f - f).functionValues[v] == f.functionValues[v] - f.functionValues[v]
    assert (f * f).functionValues[v] == f.functionValues[v] * f.functionValues[v]

assert C.vertices == {v1, v2, v3}

assert C.getEndpointsOfEdges(v1) == {(e1, 1), (e3, 1), (e4, 1), (e4, 2), (l, 1)}
assert C.getEndpointsOfEdges(v2) == {(e1, 2), (e2, 1)}
assert C.getEndpointsOfEdges(v3) == {(e2, 2), (e3, 2)}

assert C.degree(v1) == 5
assert C.degree(v2) == 2
assert C.degree(v3) == 2

assert C.genus == 3
assert C.bettiNumber == 2

subdiv = C.getSubdivision(e4, 0.5)
assert subdiv.degree(v1) == 5
assert subdiv.degree(v2) == 2
assert subdiv.degree(v3) == 2
assert subdiv.genus == 3
assert subdiv.bettiNumber == 2
assert subdiv.vertexNumber == C.vertexNumber + 1
assert subdiv.edgeNumber == C.edgeNumber + 1














C = CombCurve("Exercise 3.15 part 1")
v1 = vertex("v1", 0)
v2 = vertex("v2", 0)
v3 = vertex("v3", 0)
e1 = edge("e1", 1.0, v1, v2)
e2 = edge("e2", 1.0, v1, v3)
e3 = edge("e3", 1.0, v1, v3)
e4 = edge("e4", 1.0, v2, v3)
e5 = edge("e5", 1.0, v1, v1)
e6 = edge("e6", 1.0, v2, v2)
e7 = edge("e7", 1.0, v3, v3)
C.edges = {e1, e2, e3, e4, e5, e6, e7}
assert C.bettiNumber == 5
assert C.genus == 5










C = CombCurve("Exercise 3.15 parts 2 and 3")
v1 = vertex("v1", 1)
v2 = vertex("v2", 1)
v3 = vertex("v3", 1)
v4 = vertex("v4", 1)
v5 = vertex("v5", 1)
C.edges = {edge("e1", 1.0, v1, v2), edge("e2", 1.0, v2, v3), edge("e3", 1.0, v3, v4), edge("e4", 1.0, v4, v5)}
assert C.bettiNumber == 0
assert C.genus == 5
for v in C.vertices:
    assert v.genus <= 1







C = CombCurve("Curve with some vertices missing")
v1 = vertex("v1", 1)
e1 = edge("e1", 1.0, v1, v1)
e2 = edge("e2", 1.0, v1, None)
e3 = edge("e3", 1.0, None, None)
C.edges = {e1, e2, e3}

assert C.bettiNumber == 1
assert C.genus == 2
assert C.vertices == {v1}
assert C.edgesWithVertices == {e1}
assert C.edges == {e1, e2, e3}

dict = {v1: 1.0}

f = StrictPiecewiseLinearFunction(C, dict)





"""
# Test out some specialization code
m = TropicalModuliSpace(1, 3)
C = CombCurve("Specialization Test Curve")
v = vertex("v", 2)
leg1 = leg("leg1", v)
leg2 = leg("leg2", v)
leg3 = leg("leg3", v)

C.legs = {leg1, leg2, leg3}

print("Before specialization:")
C.showVertices()
C.showEdges()
C.showLegs()
print("Graph structure of ", C.name)
for e in C.edges:
    print("Vertices of edge ", e.name, ": (", e.vert1.name, ", ", e.vert2.name, ")")
for l in C.legs:
    print ("Root of leg ", l.name, ": ", l.root.name)
print("After splitting v:")
m.specializeBySplittingAtVertex(C, v, 1, 1, {(leg1, 1)}, {(leg2, 1), (leg3, 1)})
C.showVertices()
C.showEdges()
C.showLegs()
print("Graph structure of ", C.name)
for e in C.edges:
    print("Vertices of edge ", e.name, ": (", e.vert1.name, ", ", e.vert2.name, ")")
for l in C.legs:
    print ("Root of leg ", l.name, ": ", l.root.name)






m = TropicalModuliSpace(1, 3)
C = CombCurve("Specialization Test Curve")
v = vertex("v", 2)
leg1 = leg("leg1", v)
leg2 = leg("leg2", v)
leg3 = leg("leg3", v)

C.legs = {leg1, leg2, leg3}

print("Before specialization:")
C.showVertices()
C.showEdges()
C.showLegs()
print("Graph structure of ", C.name)
for e in C.edges:
    print("Vertices of edge ", e.name, ": (", e.vert1.name, ", ", e.vert2.name, ")")
for l in C.legs:
    print ("Root of leg ", l.name, ": ", l.root.name)
print("After genus reducing v:")
m.specializeByReducingGenus(C, v)
C.showVertices()
C.showEdges()
C.showLegs()
print("Graph structure of ", C.name)
for e in C.edges:
    print("Vertices of edge ", e.name, ": (", e.vert1.name, ", ", e.vert2.name, ")")
for l in C.legs:
    print ("Root of leg ", l.name, ": ", l.root.name)
"""









C = CombCurve("Isomorphism Domain")
D = CombCurve("Isomorphism Codomain")

v1 = vertex("v1", 0)
v2 = vertex("v2", 1)
s1 = leg("s1", v1)
s2 = leg("s2", v2)
w1 = vertex("w1", 1)
t1 = leg("t1", w1)

C.legs = {s1}
D.legs = {t1}

assert C.isIsomorphicTo(C)
assert C.isIsomorphicTo(C.getFullyShallowCopy())

assert not C.isIsomorphicTo(D)

C.legs = {s2}

assert C.isIsomorphicTo(D)

# Generate some small, known, moduli spaces

m11 = TropicalModuliSpace(1, 1)
m11.generateSpaceDFS()
assert len(m11.curves) == 2

m12 = TropicalModuliSpace(1, 2)
m12.generateSpaceDFS()
assert len(m12.curves) == 5

m13 = TropicalModuliSpace(1, 3)
m13.generateSpaceDFS()
assert len(m13.curves) == 11

m14 = TropicalModuliSpace(1, 4)
m14.generateSpaceDFS()
assert len(m14.curves) == 30

m15 = TropicalModuliSpace(1, 5)
m15.generateSpaceDFS()
assert len(m15.curves) == 76

m22 = TropicalModuliSpace(2, 2)
m22.generateSpaceDFS()
assert len(m22.curves) == 60


def testTimeAndSize(g, n):
    m = TropicalModuliSpace(g, n)

    start_time = time.time()
    m.generateSpaceDFS()
    end_time = time.time()

    print("\n")
    print("Finished M(", g, ", ", n, ") in ", end_time - start_time, " seconds.")
    print("M(", g, ", ", n, ") has ", len(m.curves), " elements.")
    print("\n")


testTimeAndSize(2, 2)

print("If you see this, then all previous assertations were true!")