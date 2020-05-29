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

C.addEdges({e1, e2, e3, e4})
C.addLeg(l)

core = C.core

assert core.isConnected
assert core.genus == C.genus


dict = {v1: 1.0, v2: 0.0, v3: 0.0, l: 0.0}

f = StrictPiecewiseLinearFunction(C, dict)

s = f.getSpecialSupportPartition()

# For now we can say, that f is a mesa until we discuss.
assert f.mesaTest

assert s == [{e1, e3, e4}]

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

subdiv, copyInfo = C.getSubdivision(e4, 0.5, returnCopyInfo=True)
assert subdiv.degree(copyInfo[v1]) == 5
assert subdiv.degree(copyInfo[v2]) == 2
assert subdiv.degree(copyInfo[v3]) == 2
assert subdiv.bettiNumber == 2
assert subdiv.genus == 3
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
C.addEdges({e1, e2, e3, e4, e5, e6, e7})
assert C.bettiNumber == 5
assert C.genus == 5










C = CombCurve("Exercise 3.15 parts 2 and 3")
v1 = vertex("v1", 1)
v2 = vertex("v2", 1)
v3 = vertex("v3", 1)
v4 = vertex("v4", 1)
v5 = vertex("v5", 1)
C.addEdges({edge("e1", 1.0, v1, v2), edge("e2", 1.0, v2, v3), edge("e3", 1.0, v3, v4), edge("e4", 1.0, v4, v5)})
assert C.bettiNumber == 0
assert C.genus == 5
for v in C.vertices:
    assert v.genus <= 1







C = CombCurve("Curve with some vertices missing")
v1 = vertex("v1", 1)
e1 = edge("e1", 1.0, v1, v1)
e2 = edge("e2", 1.0, v1, None)
e3 = edge("e3", 1.0, None, None)
C.addEdges({e1, e2, e3})

assert C.bettiNumber == 1
assert C.genus == 2
assert C.vertices == {v1}
assert C.edgesWithVertices == {e1}
assert C.edges == {e1, e2, e3}

dict = {v1: 1.0}

f = StrictPiecewiseLinearFunction(C, dict)


# Test the core property
C = CombCurve("Example 3.5")
v1 = vertex("v1", 0)
v2 = vertex("v2", 0)
v3 = vertex("v3", 1)
e1 = edge("e1", 1.0, v1, v2)
e2 = edge("e2", 1.0, v2, v3)
e3 = edge("e3", 1.0, v1, v3)
e4 = edge("e4", 1.0, v1, v1)
l = leg("l", v1)

C.addEdges({e1, e3, e4})
C.addLeg(l)

core_ = C.core

#core_.showVertices()
#core_.showEdges()

assert core_.isConnected
assert core_.genus == C.genus
assert core_.vertices == {v1, v3} 




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
e1 = edge("e1", 1.0, v1, v2)
e2 = edge("e2", 1.0, v2, v3)
e3 = edge("e3", 1.0, v3, v4)
e4 = edge("e4", 1.0, v4, v5)
e5 = edge("e5", 1.0, v5, v6)
e6 = edge("e6", 1.0, v6, v7)
e7 = edge("e7", 1.0, v7, v8)
e8 = edge("e8", 1.0, v8, v9)

C.addEdges({e1, e2, e3, e4, e5, e6, e7, e8})

f = StrictPiecewiseLinearFunction(C, {v1: 0.0, v2: 1.0, v3: 0.0, v4: 1.0, v5: 0.0, v6: 0.0, v7: 1.0, v8: 1.0, v9: 0.0})



#supportEdges, supportVertices = f.getSpecialSupport()
#for e in supportEdges:
#    print(e.name)
#for v in supportVertices:
#    print(v.name)
s = f.getSpecialSupportPartition()
#print(s)
#for x in s:
#    print("Next support block:")
#    for e in x:
#        print(e.name)

# Python doesn't allow sets of mutable sets, so we convert these to sets of immutable sets before comparing
assert {frozenset(block) for block in s} == {frozenset({e1, e2}), frozenset({e3, e4}), frozenset({e6, e7, e8})}


# Example 4.4
Ex44 = CombCurve("Example 4.4")
v1 = vertex("v1", 0)
v2 = vertex("v2", 0)
v3 = vertex("v3", 0)
v4 = vertex("v4", 0)
v5 = vertex("v5", 0)
v6 = vertex("v6", 0)
e1 = edge("e1", 2.0, v1, v2)
e2 = edge("e2", 1.0, v2, v3)
e3 = edge("e3", 1.0, v3, v4)
e4 = edge("e4", 1.0, v4, v5)
e5 = edge("e5", 1.0, v4, v6)
e6 = edge("e6", 1.0, v2, v2)
l1 = leg("l1", v1)
l2 = leg("l2", v1)
l3 = leg("l3", v5)
l4 = leg("l4", v5)
l5 = leg("l5", v6)
l6 = leg("l6", v6)

Ex44.addEdges({e1, e2, e3, e4, e5})
# Ex44.legs = {l1, l2, l3, l4, l5, l6}

g = StrictPiecewiseLinearFunction(Ex44, {v1: 0.0, v2: 2.0, v3: 2.0 , v4: 1.0, v5: 0.0, v6: 0.0})

assert g.mesaTest


Ex28May = CombCurve("28")
v1 = vertex("v1", 1)
v2 = vertex("v2", 0)
v3 = vertex("v3", 0)
v4 = vertex("v4", 0)
e1 = edge("e1", 1.0, v1, v2)
e2 = edge("e2", 1.0, v2, v3)
e3 = edge("e3", 2.0, v1, v4)

Ex28May.addEdges({e1, e2, e3})

h = StrictPiecewiseLinearFunction(Ex28May, {v1: 2.0, v2: 1.0, v3: 0.0, v4: 0.0})

assert h.mesaTest







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

C.addLeg(s1)
D.addLeg(t1)

assert C.isIsomorphicTo(C)
assert C.isIsomorphicTo(C.getFullyShallowCopy())

assert not C.isIsomorphicTo(D)

C.removeLeg(s1)
C.addLeg(s2)

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


testTimeAndSize(2, 4)

print("Loading curves from file.")
m12.loadModuliSpaceFromFile("SavedModuliSpaces/M-1-2.txt")
print("Curves loaded. Printing now.")
for curve in m12.curves:
    curve.printSelf()

print("If you see this, then all previous assertations were true!")