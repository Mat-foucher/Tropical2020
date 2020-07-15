
from Tropical2020.basic_families.BasicFamily import *
from Tropical2020.basic_families.RPC import Monoid


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


def test_example_3_5():
    C = BasicFamily("Example 3.5")

    v1 = Vertex("v1", 0)
    v2 = Vertex("v2", 0)
    v3 = Vertex("v3", 1)
    # Take all edges to be of the same length (for sake of mesa testing)
    e1 = Edge("e1", freeElementA, v1, v2)
    e2 = Edge("e2", freeElementA, v2, v3)
    e3 = Edge("e3", freeElementA, v1, v3)
    e4 = Edge("e4", freeElementA, v1, v1)
    leg = Leg("l", v1)

    C.addEdges({e1, e2, e3, e4})
    C.addLeg(leg)
    C.monoid = freeMonoid

    CurveTests.verifyStructure(C, {v1, v2, v3}, {e1, e2, e3, e4}, {leg})

    CurveTests.testCore(C)

    TreeTests.testTreeAt(C, v1)
    TreeTests.testTreeAt(C, v2)
    TreeTests.testTreeAt(C, v3)
    TreeTests.verifyLoops(C, {frozenset({e4}), frozenset({e1, e2, e3})})

    CurveTests.verifyAndTestEndpointsOfEdges(C, v1, {(e1, 1), (e3, 1), (e4, 1), (e4, 2), (leg, 1)})
    CurveTests.verifyAndTestEndpointsOfEdges(C, v2, {(e1, 2), (e2, 1)})
    CurveTests.verifyAndTestEndpointsOfEdges(C, v3, {(e2, 2), (e3, 2)})

    CurveTests.verifyDegree(C, v1, 5)
    CurveTests.verifyDegree(C, v2, 2)
    CurveTests.verifyDegree(C, v3, 2)
    CurveTests.verifyGenus(C, 3)
    CurveTests.verifyBettiNumber(C, 2)


def test_example_3_15_1():
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
    # TreeTests.verifyLoops(C, {frozenset({e1, e3, e4}), frozenset({e2, e3}), frozenset({e5}), frozenset({e6}), \
    # frozenset({e7})})


def test_example_3_15_2and3():
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


def test_isos():
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
