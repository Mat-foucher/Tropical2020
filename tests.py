from CombinatorialCurve import *
from StrictPiecewiseLinearFunction import *







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

dict = {v1: 1.0, v2: 0.0, v3: 0.0, l: 0.0}

f = StrictPiecewiseLinearFunction(C, dict)

s = f.getSpecialSupportPartition()

assert not f.mesaTest()

#print(s)
assert s == [{e1, e3, e4}]
#for x in s:
#    for e in x:
#        print(e.name)

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

C.edges = {e1, e3, e4}
C.legs = {l}

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

C.edges = {e1, e2, e3, e4, e5, e6, e7, e8}

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
v2 = vertex("v2", 1)
v3 = vertex("v3", 0)
v4 = vertex("v4", 0)
v5 = vertex("v5", 0)
v6 = vertex("v6", 0)
e1 = edge("e1", 2.0, v1, v2)
e2 = edge("e2", 1.0, v2, v3)
e3 = edge("e3", 1.0, v3, v4)
e4 = edge("e4", 1.0, v4, v5)
e5 = edge("e5", 1.0, v4, v6)
l1 = leg("l1", v1)
l2 = leg("l2", v2)
l3 = leg("l3", v5)
l4 = leg("l4", v5)
l5 = leg("l5", v6)
l6 = leg("l6", v6)

Ex44.edges = {e1, e2, e3, e4, e5}
#Ex44.legs = {l1, l2, l3, l4, l5, l6}

g = StrictPiecewiseLinearFunction(Ex44, {v1: 0.0, v2: 2.0, v3: 2.0 , v4: 1.0, v5: 0.0, v6: 0.0})

assert g.mesaTest()









print("If you see this, then all previous assertations were true!")