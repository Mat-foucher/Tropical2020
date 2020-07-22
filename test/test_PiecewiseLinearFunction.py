
from Tropical2020.basic_families.PiecewiseLinearFunction import *


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


def test_example_3_5_funcs():
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

    zeroDict = {e1: 0, e2: 0, e3: 0, e4: 0,
                leg: 0,
                v1: freeMonoid.zero()}
    f = PiecewiseLinearFunction(C, zeroDict)
    SPLFTests.verifyMesa(f)

    nonMesaDict = {e1: -1, e2: 0, e3: -1, e4: 0,
                   leg: 0,
                   v2: freeMonoid.zero()}
    f = PiecewiseLinearFunction(C, nonMesaDict)

    # contractions = f.functionContractions()

    # for e in contractions:
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


def test_chain_of_9_verts():
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


def test_example_4_4():
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


def test_example_may_28():
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
