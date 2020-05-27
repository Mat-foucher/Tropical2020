from CombinatorialCurve import *
import copy
import time


class TropicalModuliSpace(object):
    def __init__(self, g_, n_):
        self._g = g_
        self._n = n_
        self._curves = set()
        # Curves organized by number of edges
        self._curvesDict = {}

    @property
    def curves(self):
        return self._curves

    @curves.setter
    def curves(self, curves_):
        self._curves = curves_

    @property
    def curvesDict(self):
        return self._curvesDict

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
            partition.append((S | {elem}, T))
            partition.append((S, T | {elem}))

        return partition

    def reduceByIsomorphism(self, curves=None):

        modifySelf = (curves is None)
        if modifySelf:

            for n in self.curvesDict:
                self.curvesDict[n] = self.reduceByIsomorphism(self.curvesDict[n])
            self.curves = set()
            for n in self.curvesDict:
                self.curves = self.curves | set(self.curvesDict[n])
            return self.curves
        else:
            isotypes = []
            for curve in curves:
                newIsotype = True
                for t in isotypes:
                    if t[0].isIsomorphicTo(curve):
                        t.append(curve)
                        newIsotype = False
                        break
                if newIsotype:
                    isotypes.append([curve])
            return {t[0] for t in isotypes}

    def containsUpToIsomorphism(self, curve):

        if curve.edgeNumber not in self.curvesDict:
            return False
        else:
            for c in self.curvesDict[curve.edgeNumber]:
                if c.isIsomorphicTo(curve):
                    return True

        return False

    def addCurve(self, curve):
        # if not self.containsUpToIsomorphism(curve):
        #     self.curves = self.curves | {curve}

        numEdges = curve.edgeNumber
        if numEdges in self.curvesDict:
            curveIsNew = True
            for c in self.curvesDict[numEdges]:
                if curve.isIsomorphicTo(c):
                    curveIsNew = False
                    break
            if curveIsNew:
                self.curvesDict[numEdges] = self.curvesDict[numEdges] + [curve]
                self.curves = self.curves | {curve}
                #print("Currently at ", len(self.curves), " curves.")
        else:
            self.curvesDict[numEdges] = [curve]
            self.curves = self.curves | {curve}

    def addSpecializationsDFS(self, curve):
        newCurves = []

        # Get the one-step specializations of the given curve
        for vert in curve.vertices:

            # If the genus of vert is positive, then we can decrement its genus and add a self loop
            if vert.genus > 0:
                genusReducedCurve = self.getGenusReductionSpecialization(curve, vert)
                newCurves.append(genusReducedCurve)

            # We can also split a vertex in two and pass around parts of its genus and endpoints to the new pieces
            endpointPartitions = self.getPartitions(curve.getEndpointsOfEdges(vert))

            # Anticipate some isomorphic results
            endpointPartitions = [(S, T) for (S, T) in endpointPartitions if len(S) <= len(T)]

            for g in range(vert.genus + 1):
                for p in endpointPartitions:
                    S, T = p
                    if not ((g == 0 and len(S) < 2) or (g == vert.genus and len(T) < 2)):
                        vertexSplitCurve = self.getSplittingSpecialization(curve, vert, g, vert.genus - g, S, T)
                        newCurves.append(vertexSplitCurve)

        # Reduce before we go down a level
        newCurvesBuffer = self.reduceByIsomorphism(newCurves)
        newCurves = []
        for c in newCurvesBuffer:
            if not self.containsUpToIsomorphism(c):
                newCurves.append(c)
                self.addCurve(c)

        #print("Found ", len(newCurves), " new curves")
        #print("Currently have ", len(self.curves), " curves!")

        # Specialize the specializations DFS
        for c in newCurves:
            self.addSpecializationsDFS(c)

    def generateSpaceDFS(self):

        # start_time = time.time()

        seedCurve = CombCurve("Seed curve with genus " + str(self._g) + ", " + str(self._n) + " legs, and 0 edges")
        v = vertex("v", self._g)
        seedCurve.legs = {leg("leg " + str(i), v) for i in range(self._n)}

        self.addCurve(seedCurve)
        self.addSpecializationsDFS(seedCurve)

        # generation_complete_time = time.time()

        # print("Generation time: ", generation_complete_time - start_time)

    def generateSpace(self, suppressComments=True):

        seedCurve = CombCurve("Seed curve with genus " + str(self._g) + ", " + str(self._n) + " legs, and 0 edges")
        v = vertex("v", self._g)
        seedCurve.legs = {leg("leg " + str(i), v) for i in range(self._n)}

        self._curves = self._curves | {seedCurve}

        newCurves = [seedCurve]

        while newCurves:
            if not suppressComments:
                print("Found ", len(newCurves), " new curves. Reducing now.")
            curveBuffer = list(self.reduceByIsomorphism(newCurves))
            if not suppressComments:
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
        c, copyInfo = curve.getFullyShallowCopy(True)
        c.name = "(Spec. of " + curve.name + " from genus reducing at " + vert.name

        self.specializeByReducingGenus(c, copyInfo[vert])
        return c
