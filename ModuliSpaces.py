from CombinatorialCurve import *

class TropicalModuliSpace(object):
    def __init__(self, g_, n_):
        self._g = g_
        self._n = n_

    # unique space of genus g, n marked, with zero edges:
    # seedCurve = CombCurve("seed")
    # v = vertex("v", g)
    # seedCurve.legs = {leg("leg " + i, v) for i in range(n)}

    # Returns the specialization of 'curve' at 'vert' as determined by g1, g2, S, and T
    # Specifically, 'vert' is split into two vertices, v1 and v2, of genuses g1 and g2 respectively, where g1+g2 == vert.genus
    # S and T partition the endpoints of edges on vert, and we move the endpoints of edges in S to v1 and those in T to v2
    def specializeAtVertex(self, curve, vert, g1, g2, S, T):
        assert g1 + g2 == vert.genus
        v1 = vertex("(First split of " + vert.name + ")", g1)
        v2 = vertex("(Second split of " + vert.name + ")", g2)

        for p in S:
            e, edgeNum = p
            if isinstance(e, edge):
                if edgeNum == 1:
                    e.vert1 = v1
                else:
                    e.vert2 = v1
            else:
                e.root = v1

        for p in T:
            e, edgeNum = p
            if isinstance(e, edge):
                if edgeNum == 1:
                    e.vert1 = v2
                else:
                    e.vert2 = v2
            else:
                e.root = v2

        e = edge("(Edge splitting " + vert.name + ")", 1.0, v1, v2)

        curve.edges = curve.edges | {e}