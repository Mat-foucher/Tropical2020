from CombinatorialCurve import *
from StrictPiecewiseLinearFunction import *
from ModuliSpaces import *
import time


class CurveTests:
    @staticmethod
    def verifyStructure(curve, verts, edges, legs):
        assert curve.vertices == verts
        assert curve.edges == edges
        assert curve.legs == legs

    @staticmethod
    def verifyDegree(curve, vert, deg):
        assert curve.degree(vert) == deg

    @staticmethod
    def verifyGenus(curve, genus):
        assert curve.genus == genus

    @staticmethod
    def verifyBettiNumber(curve, bettiNum):
        assert curve.bettiNumber == bettiNum

    @staticmethod
    def testCore(curve):
        assert curve.core.isConnected
        assert curve.core.genus == curve.genus

    @staticmethod
    def verifyConnectedness(curve, connected=True):
        assert curve.isConnected == connected

    @staticmethod
    def verifyAndTestEndpointsOfEdges(curve, vert, endpoints):
        assert curve.getEndpointsOfEdges(vert) == endpoints
        assert len(endpoints) == curve.edgeDegree(vert) + curve.legDegree(vert)

    @staticmethod
    def verifyIsomorphism(curve1, curve2, isIsomorphic=True):
        assert curve1.isIsomorphicTo(curve2) == isIsomorphic


class SPLFTests:
    @staticmethod
    def verifyMesa(func, isMesa=True):
        assert func.mesaTest == isMesa

    @staticmethod
    def verifySpecialSupport(func, supportBlocks):
        assert func.getSpecialSupportPartition() == supportBlocks

    @staticmethod
    def testSelfArithmetic(func):
        for vert in func.domain.vertices:
            assert (func + func).functionValues[vert] == func.functionValues[vert] + func.functionValues[vert]
            assert (func - func).functionValues[vert] == func.functionValues[vert] - func.functionValues[vert]
            assert (func * func).functionValues[vert] == func.functionValues[vert] * func.functionValues[vert]


class TreeTests:
    @staticmethod
    def testTreeAt(curve, vert):
        tree = curve.getSpanningTree(vert)
        # The tree must be a spanning tree
        assert tree.getVertices() == curve.vertices
        # The betti number of a tree must be zero
        assert len(tree.getVertices()) == len(tree.getEdges()) + 1

    @staticmethod
    def verifyLoops(curve, loops):
        curveLoops = set()
        for loop in curve.loops:
            curveLoops.add(frozenset(loop))
        assert curveLoops == loops


class ModuliSpaceTests:
    @staticmethod
    def verifyCommonSizes():
        m10 = TropicalModuliSpace(1, 0)
        m10.generateSpaceDFS()
        assert len(m10.curves) == 1

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




m = TropicalModuliSpace(1, 2)
m.generateSpaceDFS()
m.generateContractionDictionary()
for curve in m.curves:
    curve.printSelf()

for key in m.contractionDict:
    print("Printing contraction info for the following curve:")
    key.printSelf()
    for p in m.contractionDict[key]:
            contraction = p[0]
            e = p[1]
            print("Contracting edge", e.name, "produces the following curve:")
            contraction.printSelf()








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

#contraction = C.getContraction(e4)
#print("Printing contraction:")
#contraction.printSelf()
#contraction = C.getContraction(e2)
#contraction.simplifyNames()
#print("Printing contraction:")
#contraction.printSelf()

CurveTests.verifyStructure(C, {v1, v2, v3}, {e1, e2, e3, e4}, {l})

CurveTests.testCore(C)

TreeTests.testTreeAt(C, v1)
TreeTests.testTreeAt(C, v2)
TreeTests.testTreeAt(C, v3)
TreeTests.verifyLoops(C, {frozenset({e4}), frozenset({e1, e2, e3})})

dict = {v1: 1.0, v2: 0.0, v3: 0.0, l: 0.0}
f = StrictPiecewiseLinearFunction(C, dict)

SPLFTests.verifyMesa(f, isMesa=False)
SPLFTests.verifySpecialSupport(f, [{e1, e3, e4}])
SPLFTests.testSelfArithmetic(f)

CurveTests.verifyAndTestEndpointsOfEdges(C, v1, {(e1, 1), (e3, 1), (e4, 1), (e4, 2), (l, 1)})
CurveTests.verifyAndTestEndpointsOfEdges(C, v2, {(e1, 2), (e2, 1)})
CurveTests.verifyAndTestEndpointsOfEdges(C, v3, {(e2, 2), (e3, 2)})

CurveTests.verifyDegree(C, v1, 5)
CurveTests.verifyDegree(C, v2, 2)
CurveTests.verifyDegree(C, v3, 2)
CurveTests.verifyGenus(C, 3)
CurveTests.verifyBettiNumber(C, 2)

subdiv, copyInfo = C.getSubdivision(e4, 0.5, returnCopyInfo=True)
CurveTests.verifyDegree(subdiv, copyInfo[v1], C.degree(v1))
CurveTests.verifyDegree(subdiv, copyInfo[v2], C.degree(v2))
CurveTests.verifyDegree(subdiv, copyInfo[v3], C.degree(v3))
CurveTests.verifyGenus(subdiv, C.genus)
CurveTests.verifyBettiNumber(subdiv, C.bettiNumber)
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
CurveTests.verifyGenus(C, 5)
CurveTests.verifyBettiNumber(C, 5)
# Do not uncomment the following line of code - a basis of loops for this curve is NOT unique.
# This line has been retained so it isn't added back in later.
# TreeTests.verifyLoops(C, {frozenset({e1, e3, e4}), frozenset({e2, e3}), frozenset({e5}), frozenset({e6}), frozenset({e7})})

# for loop in C.loops:
#     print("Printing a loop")
#     for e in loop:
#         print(e.name)








C = CombCurve("Exercise 3.15 parts 2 and 3")
v1 = vertex("v1", 1)
v2 = vertex("v2", 1)
v3 = vertex("v3", 1)
v4 = vertex("v4", 1)
v5 = vertex("v5", 1)
C.addEdges({edge("e1", 1.0, v1, v2), edge("e2", 1.0, v2, v3), edge("e3", 1.0, v3, v4), edge("e4", 1.0, v4, v5)})
CurveTests.verifyGenus(C, 5)
CurveTests.verifyBettiNumber(C, 0)
for v in C.vertices:
    assert v.genus <= 1
TreeTests.verifyLoops(C, set())







C = CombCurve("Curve with some vertices missing")
v1 = vertex("v1", 1)
e1 = edge("e1", 1.0, v1, v1)
e2 = edge("e2", 1.0, v1, None)
e3 = edge("e3", 1.0, None, None)
C.addEdges({e1, e2, e3})

CurveTests.verifyGenus(C, 2)
CurveTests.verifyBettiNumber(C, 1)
CurveTests.verifyStructure(C, {v1}, {e1, e2, e3}, set())
assert C.edgesWithVertices == {e1}

f = StrictPiecewiseLinearFunction(C, {v1: 1.0})


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

CurveTests.testCore(C)
CurveTests.verifyStructure(C.core, {v1, v3}, {e3, e4}, set())




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
e6 = edge("e6", 1.0, v2, v2)
l1 = leg("l1", v1)
l2 = leg("l2", v1)
l3 = leg("l3", v5)
l4 = leg("l4", v5)
l5 = leg("l5", v6)
l6 = leg("l6", v6)

Ex44.addEdges({e1, e2, e3, e4, e5})
Ex44.addLegs({l1, l2, l3, l4, l5, l6})

g = StrictPiecewiseLinearFunction(Ex44, {v1: 0.0, v2: 2.0, v3: 2.0, v4: 1.0, v5: 0.0, v6: 0.0,
                                         l1: 0.0, l2: 0.0, l3: 0.0, l4: 0.0, l5: 0.0, l6: 0.0})

SPLFTests.verifyMesa(g)


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

SPLFTests.verifyMesa(h)







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

CurveTests.verifyIsomorphism(C, C)
CurveTests.verifyIsomorphism(C, C.getFullyShallowCopy())

CurveTests.verifyIsomorphism(C, D, False)

C.removeLeg(s1)
C.addLeg(s2)

CurveTests.verifyIsomorphism(C, D)

# Generate some small, known, moduli spaces
ModuliSpaceTests.verifyCommonSizes()


print("If you see this, then all previous assertations were true!")
