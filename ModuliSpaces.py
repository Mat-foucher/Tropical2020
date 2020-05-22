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
    def specializeAtVertex(curve, vert, g1, g2, S, T):
        pass