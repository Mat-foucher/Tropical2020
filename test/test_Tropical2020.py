from Tropical2020.basic_families.BasicFamily import *
from Tropical2020.basic_families.PiecewiseLinearFunction import *
from Tropical2020.general_families.ModuliSpace import *
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






"""
print("Starting new load tests for M-1-2...")
m = TropicalModuliSpace(1, 2)
m.loadModuliSpaceFromFile("SavedModuliSpaces/M-1-2.txt")
print("Done loading space. Printing curves now...")
for curve in m.curves:
    print("")
    curve.printSelf()
print("Done printing curves. Printing contraction data now...")
for curve in m.curves:
    print("\nPrinting contraction info for the following curve:")
    curve.printSelf()
    for e in curve.edges:
        print("Contracting", e.name, 'produces the following curve:')
        # Filtering a list doesn't produce a list :'(
        for p in filter(lambda x: x[0] == e, m.contractionDict[curve]):
            p[1].printSelf()
            break
"""


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




C = BasicFamily("Example 3.5")

v1 = Vertex("v1", 0)
v2 = Vertex("v2", 0)
v3 = Vertex("v3", 1)
# Take all edges to be of the same length (for sake of mesa testing)
e1 = Edge("e1", freeElementA, v1, v2)
e2 = Edge("e2", freeElementA, v2, v3)
e3 = Edge("e3", freeElementA, v1, v3)
e4 = Edge("e4", freeElementA, v1, v1)
l = Leg("l", v1)

C.addEdges({e1, e2, e3, e4})
C.addLeg(l)
C.monoid = freeMonoid

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

zeroDict = {e1: 0, e2: 0, e3: 0, e4: 0,
            l: 0,
            v1: freeMonoid.zero()}
f = PiecewiseLinearFunction(C, zeroDict)
SPLFTests.verifyMesa(f)

nonMesaDict = {e1: -1, e2: 0, e3: -1, e4: 0,
               l: 0,
               v2: freeMonoid.zero()}
f = PiecewiseLinearFunction(C, nonMesaDict)

#contractions = f.functionContractions()

#for e in contractions:
#    print(" ")
#    print(e.name, "Contractions:")
#    contractions[e].printSelf()

SPLFTests.verifyMesa(f, isMesa=False)
try:
    SPLFTests.verifySpecialSupport(f, [{e1, e3, e4}])
except:
    print("Test failed! Here's the problematic function and support:")
    print("Examining the following function:")
    f.printSelf()
    print("Special support...")
    for block in f.getSpecialSupportPartition():
        print("Next block:")
        for e in block:
            print(e.name)



SPLFTests.testSelfArithmetic(f)

CurveTests.verifyAndTestEndpointsOfEdges(C, v1, {(e1, 1), (e3, 1), (e4, 1), (e4, 2), (l, 1)})
CurveTests.verifyAndTestEndpointsOfEdges(C, v2, {(e1, 2), (e2, 1)})
CurveTests.verifyAndTestEndpointsOfEdges(C, v3, {(e2, 2), (e3, 2)})

CurveTests.verifyDegree(C, v1, 5)
CurveTests.verifyDegree(C, v2, 2)
CurveTests.verifyDegree(C, v3, 2)
CurveTests.verifyGenus(C, 3)
CurveTests.verifyBettiNumber(C, 2)














C = BasicFamily("Exercise 3.15 part 1")
v1 = Vertex("v1", 0)
v2 = Vertex("v2", 0)
v3 = Vertex("v3", 0)
e1 = Edge("e1", 1.0, v1, v2)
e2 = Edge("e2", 1.0, v1, v3)
e3 = Edge("e3", 1.0, v1, v3)
e4 = Edge("e4", 1.0, v2, v3)
e5 = Edge("e5", 1.0, v1, v1)
e6 = Edge("e6", 1.0, v2, v2)
e7 = Edge("e7", 1.0, v3, v3)
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








C = BasicFamily("Exercise 3.15 parts 2 and 3")
v1 = Vertex("v1", 1)
v2 = Vertex("v2", 1)
v3 = Vertex("v3", 1)
v4 = Vertex("v4", 1)
v5 = Vertex("v5", 1)
C.addEdges({Edge("e1", 1.0, v1, v2), Edge("e2", 1.0, v2, v3), Edge("e3", 1.0, v3, v4), Edge("e4", 1.0, v4, v5)})
CurveTests.verifyGenus(C, 5)
CurveTests.verifyBettiNumber(C, 0)
for v in C.vertices:
    assert v.genus <= 1
TreeTests.verifyLoops(C, set())







#C = BasicFamily("Curve with some vertices missing")
#v1 = Vertex("v1", 1)
#e1 = Edge("e1", 1.0, v1, v1)
#e2 = Edge("e2", 1.0, v1, None)
#e3 = Edge("e3", 1.0, None, None)
#C.addEdges({e1, e2, e3})

#CurveTests.verifyGenus(C, 2)
#CurveTests.verifyBettiNumber(C, 1)
#CurveTests.verifyStructure(C, {v1}, {e1, e2, e3}, set())
#assert C.edgesWithVertices == {e1}

#f = StrictPiecewiseLinearFunction(C, {v1: 1.0})


# Test the core property
C = BasicFamily("Example 3.5")
v1 = Vertex("v1", 0)
v2 = Vertex("v2", 0)
v3 = Vertex("v3", 1)
e1 = Edge("e1", 1.0, v1, v2)
e2 = Edge("e2", 1.0, v2, v3)
e3 = Edge("e3", 1.0, v1, v3)
e4 = Edge("e4", 1.0, v1, v1)
l = Leg("l", v1)

C.addEdges({e1, e3, e4})
C.addLeg(l)

CurveTests.testCore(C)
CurveTests.verifyStructure(C.core, {v1, v3}, {e3, e4}, set())




C = BasicFamily("Chain of 9 vertices")
v1 = Vertex("v1", 0)
v2 = Vertex("v2", 0)
v3 = Vertex("v3", 0)
v4 = Vertex("v4", 0)
v5 = Vertex("v5", 0)
v6 = Vertex("v6", 0)
v7 = Vertex("v7", 0)
v8 = Vertex("v8", 0)
v9 = Vertex("v9", 0)
e1 = Edge("e1", freeElementA, v1, v2)
e2 = Edge("e2", freeElementA, v2, v3)
e3 = Edge("e3", freeElementA, v3, v4)
e4 = Edge("e4", freeElementA, v4, v5)
e5 = Edge("e5", freeElementA, v5, v6)
e6 = Edge("e6", freeElementA, v6, v7)
e7 = Edge("e7", freeElementA, v7, v8)
e8 = Edge("e8", freeElementA, v8, v9)

C.addEdges({e1, e2, e3, e4, e5, e6, e7, e8})
C.monoid = freeMonoid

f = PiecewiseLinearFunction(C, {e1: 1, e2: -1, e3: 1, e4: -1, e5: 0, e6: 1, e7: 0, e8: -1,
                                v1: freeMonoid.zero()})

s = f.getSpecialSupportPartition()

try:
    # Python doesn't allow sets of mutable sets, so we convert these to sets of immutable sets before comparing
    assert {frozenset(block) for block in s} == {frozenset({e1, e2}), frozenset({e3, e4}), frozenset({e6, e7, e8})}
except:
    print("Got an error with special support partition. Here's the problematic function and partition.")
    print("Examining the following function:")
    f.printSelf()
    print("Special support...")
    for block in f.getSpecialSupportPartition():
        print("Next block:")
        for e in block:
            print(e.name)


# Example 4.4
Ex44 = BasicFamily("Example 4.4")
v1 = Vertex("v1", 0)
v2 = Vertex("v2", 1)
v3 = Vertex("v3", 0)
v4 = Vertex("v4", 0)
v5 = Vertex("v5", 0)
v6 = Vertex("v6", 0)
e1 = Edge("e1", 2 * freeElementA, v1, v2)
e2 = Edge("e2", freeElementA, v2, v3)
e3 = Edge("e3", freeElementA, v3, v4)
e4 = Edge("e4", freeElementA, v4, v5)
e5 = Edge("e5", freeElementA, v4, v6)
e6 = Edge("e6", freeElementA, v2, v2)
l1 = Leg("l1", v1)
l2 = Leg("l2", v1)
l3 = Leg("l3", v5)
l4 = Leg("l4", v5)
l5 = Leg("l5", v6)
l6 = Leg("l6", v6)

Ex44.addEdges({e1, e2, e3, e4, e5})
Ex44.addLegs({l1, l2, l3, l4, l5, l6})
Ex44.monoid = freeMonoid

g = PiecewiseLinearFunction(Ex44, {e1: 1, e2: 0, e3: -1, e4: -1, e5: -1, e6: 0,
                                   l1: 0.0, l2: 0.0, l3: 0.0, l4: 0.0, l5: 0.0, l6: 0.0,
                                   v1: freeMonoid.zero()})

SPLFTests.verifyMesa(g)


Ex28May = BasicFamily("28")
v1 = Vertex("v1", 1)
v2 = Vertex("v2", 0)
v3 = Vertex("v3", 0)
v4 = Vertex("v4", 0)
e1 = Edge("e1", freeElementA, v1, v2)
e2 = Edge("e2", freeElementA, v2, v3)
e3 = Edge("e3", 2 * freeElementA, v1, v4)

Ex28May.addEdges({e1, e2, e3})
Ex28May.monoid = freeMonoid

h = PiecewiseLinearFunction(Ex28May, {e1: -1, e2: -1, e3: -1,
                                      v3: freeMonoid.zero()})

SPLFTests.verifyMesa(h)










"""
# Test out some specialization code
m = TropicalModuliSpace(1, 3)
C = BasicFamily("Specialization Test Curve")
v = Vertex("v", 2)
leg1 = Leg("leg1", v)
leg2 = Leg("leg2", v)
leg3 = Leg("leg3", v)

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
C = BasicFamily("Specialization Test Curve")
v = Vertex("v", 2)
leg1 = Leg("leg1", v)
leg2 = Leg("leg2", v)
leg3 = Leg("leg3", v)

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









C = BasicFamily("Isomorphism Domain")
D = BasicFamily("Isomorphism Codomain")

v1 = Vertex("v1", 0)
v2 = Vertex("v2", 1)
s1 = Leg("s1", v1)
s2 = Leg("s2", v2)
w1 = Vertex("w1", 1)
t1 = Leg("t1", w1)

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
