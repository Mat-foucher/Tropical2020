from CombinatorialCurve import *
import copy


class TropicalModuliSpace(object):
    def __init__(self, g_, n_):
        self._g = g_
        self._n = n_
        self._curves = set()

    # TODO: Figure out whether python passes by reference or value so we can avoid the silly pop/add lines
    def getPartitions(self, s):

        if len(s) == 1:
            elem = s.pop()
            s.add(elem)
            return [(set(), {elem}), ({elem}, set())]

        elem = s.pop()
        s.add(elem)
        p = self.getPartitions(s - {elem})

        partition = []
        for blockPair in p:
            S, T = blockPair
            if len(S) < len(T):
                partition.append((S | {elem}, T))
            partition.append((S, T | {elem}))

        return partition

    @staticmethod
    def printCurve(curve):
        """
        print("\nPrinting a new curve")
        print("Vertices:")
        for v in curve.vertices:
            print(v.name, " with genus ", v.genus)
        for e in curve.edges:
            print("Edge ", e.name, " with vertices ", e.vert1.name, " and ", e.vert2.name)
        for l in curve.legs:
            print("Leg ", l.name, " with root ", l.root.name)
        """

        print("\n\nVertices:")
        for v in curve.vertices:
            print(v.name, " with genus ", v.genus)
        print("Edges:")
        for e in curve.edges:
            print(e.name)
        print("Legs:")
        for nextLeg in curve.legs:
            print(nextLeg.name)

    def reduceByIsomorphism(self, curves=None):
        isotypes = []

        modifySelf = (curves is None)
        if modifySelf:
            curves = self._curves

        for curve in curves:
            newIsotype = True
            for t in isotypes:
                if t[0].isIsomorphicTo(curve):
                    t.append(curve)
                    newIsotype = False
                    break
            if newIsotype:
                isotypes.append([curve])

        if modifySelf:
            self._curves = [t[0] for t in isotypes]
            return self._curves
        return [t[0] for t in isotypes]

    def generateSpace(self):

        seedCurve = CombCurve("Seed curve with genus " + str(self._g) + ", " + str(self._n) + " legs, and 0 edges")
        v = vertex("v", self._g)
        seedCurve.legs = {leg("leg " + str(i), v) for i in range(self._n)}

        self._curves = self._curves | {seedCurve}

        newCurves = [seedCurve]

        while newCurves:
            print("Found ", len(newCurves), " new curves. Reducing now.")
            curveBuffer = self.reduceByIsomorphism(newCurves)
            print("Reduced to ", len(curveBuffer), " new curves.")
            self._curves = self._curves | set(curveBuffer)
            newCurves = []
            # print("\n\n\n\n\n\n###################### Moving to next level ######################\n\n\n\n\n\n")
            while curveBuffer:
                currentCurve = curveBuffer[0]

                # print("\n\n\nCurrent curve:")
                # self.printCurve(currentCurve)

                for vert in currentCurve.vertices:

                    endpointPartitions = self.getPartitions(currentCurve.getEndpointsOfEdges(vert))

                    if vert.genus > 0:
                        # print("\nGenus reducing vertex: " + vert.name)
                        genusReducedCurve = self.getGenusReductionSpecialization(currentCurve, vert)
                        newCurves.append(genusReducedCurve)
                        # self.printCurve(genusReducedCurve)

                    for g in range(vert.genus + 1):
                        for p in endpointPartitions:
                            S, T = p
                            if not ((g == 0 and len(S) < 2) or (g == vert.genus and len(T) < 2)):
                                # print("\nSplitting vertex: " + vert.name)
                                vertexSplitCurve = self.getSplittingSpecialization(currentCurve, vert, g,
                                                                                   vert.genus - g, S, T)
                                newCurves.append(vertexSplitCurve)
                                # self.printCurve(vertexSplitCurve)
                curveBuffer.remove(currentCurve)

                # print("Current buffer length: ", len(curveBuffer))
                # print("Number of new curves this loop: ", len(newCurves))

        return self._curves

    # Returns the specialization of 'curve' at 'vert' as determined by g1, g2, S, and T
    # Specifically, 'vert' is split into two vertices, v1 and v2, of genuses g1 and g2 respectively,
    # where g1+g2 == vert.genus
    # S and T partition the endpoints of edges on vert, and we move the endpoints of edges in S to v1 and those
    # in T to v2
    @staticmethod
    def specializeBySplittingAtVertex(curve, vert, g1, g2, S, T):
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

    def getSplittingSpecialization(self, curve, vert, g1, g2, S, T):
        # copy the curve shallowly and keep track of how copying was performed
        c, copyInfo = curve.getFullyShallowCopy(True)
        c.name = "(Spec. of " + curve.name + " from splitting at " + vert.name

        safeS = set()
        safeT = set()
        for p in S:
            e, n = p
            safeS.add((copyInfo[e], n))
        for p in T:
            e, n = p
            safeT.add((copyInfo[e], n))

        # c.edges = {copy.copy(e) for e in curve.edges}
        # c.legs = {copy.copy(l) for l in curve.legs}
        self.specializeBySplittingAtVertex(c, vert, g1, g2, safeS, safeT)
        return c

    @staticmethod
    def specializeByReducingGenus(curve, vert):
        assert vert.genus > 0

        endpoints = curve.getEndpointsOfEdges(vert)

        v = vertex("(Genus reduction of " + vert.name + ")", vert.genus - 1)

        for p in endpoints:
            e, edgeNum = p
            if isinstance(e, edge):
                if edgeNum == 1:
                    e.vert1 = v
                else:
                    e.vert2 = v
            else:
                e.root = v

        e = edge("(Genus reduction loop for " + vert.name + ")", 1.0, v, v)

        curve.edges = curve.edges | {e}

    def getGenusReductionSpecialization(self, curve, vert):
        c = CombCurve("(Spec. of " + curve.name + " from genus reducing at " + vert.name)
        c.edges = {copy.copy(e) for e in curve.edges}
        c.legs = {copy.copy(nextLeg) for nextLeg in curve.legs}
        self.specializeByReducingGenus(c, vert)
        return c
