from CombinatorialCurve import *
import copy
import time

import re

class TropicalModuliSpace(object):
    def __init__(self, g_, n_):
        self._g = g_
        self._n = n_
        self._curves = set()
        # Curves organized by number of edges
        self._curvesDict = {}
        # Dictionary tracking what each curve can contract to
        # contractionDict[curve]: List[(contraction, number of ways the contraction can occur)]
        self.contractionDict = {}

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

        if len(s) == 0:
            return [(set(), set())]
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

    def reduceByIsomorphism(self, curves=None, returnReductionInformation=False):

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
            if returnReductionInformation:
                reductionDict = {}
                for t in isotypes:
                    reductionDict[t[0]] = t
                return {t[0] for t in isotypes}, reductionDict
            else:
                return {t[0] for t in isotypes}

    def containsUpToIsomorphism(self, curve, returnMatch=False):

        if curve.edgeNumber not in self.curvesDict:
            if returnMatch:
                return False, None
            else:
                return False
        else:
            for c in self.curvesDict[curve.edgeNumber]:
                if c.isIsomorphicTo(curve):
                    if returnMatch:
                        return True, c
                    else:
                        return True

        if returnMatch:
            return False, None
        else:
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
            if vert.genus > 1:
                genusReducedCurve = self.getGenusReductionSpecialization(curve, vert)
                newCurves.append(genusReducedCurve)
            elif vert.genus == 1 and curve.degree(vert) > 0:
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

        if self._g == 0 and self._n < 3:
            return

        seedCurve = CombCurve("Seed curve with genus " + str(self._g) + ", " + str(self._n) + " legs, and 0 edges")
        v = vertex("v", self._g)
        seedCurve.addVertex(v)
        seedCurve.addLegs({leg("leg " + str(i), v) for i in range(self._n)})

        self.addCurve(seedCurve)
        self.addSpecializationsDFS(seedCurve)

        # generation_complete_time = time.time()

        # print("Generation time: ", generation_complete_time - start_time)

    def generateContractionDictionary(self):
        numCurves = len(self.curves)
        it = 1
        for curve in self.curves:
            print("Working on getting contraction history of curve", str(it), "/", str(numCurves), "of M-" + str(self._g) + "-" + str(self._n))
            contractionPairs = []
            for nextEdge in curve.edges:
                contractionCurve = curve.getContraction(nextEdge)
                p = self.containsUpToIsomorphism(contractionCurve, returnMatch=True)
                containsAMatch = p[0]
                match = p[1]
                assert containsAMatch
                contractionPairs.append((match, nextEdge))
            self.contractionDict[curve] = contractionPairs
            it += 1

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

        curve.addEdge(e)
        curve.removeVertex(vert)

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
        self.specializeBySplittingAtVertex(c, copyInfo[vert], g1, g2, safeS, safeT)
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

        curve.addEdge(e)
        curve.removeVertex(vert)

    def getGenusReductionSpecialization(self, curve, vert):
        c, copyInfo = curve.getFullyShallowCopy(True)
        c.name = "(Spec. of " + curve.name + " from genus reducing at " + vert.name + ")"

        self.specializeByReducingGenus(c, copyInfo[vert])
        return c

    def loadModuliSpaceFromFile(self, filename, curveEntryDelimiter="=", encoding='utf-8'):
        self.curves = set()
        with open(filename, mode='r', encoding=encoding) as f:
            content = f.read()
            curveStrings = content.split("\n" + curveEntryDelimiter + "\n")
            curveIdDictionary = {}
            curveContractionDictionary = {}
            for curveString in curveStrings:
                curveInfo = curveString.split("\n")
                vertexInfo = curveInfo[0]
                vertexInfoFinder = re.compile("\((v\d*) with genus (\d*)\)")

                edgeInfo = curveInfo[1]
                edgeInfoFinder = re.compile("edge\((v\d*), (v\d*)\)")

                legInfo = curveInfo[2]
                legInfoFinder = re.compile("leg\((v\d*)\)")

                curveIdInfo = curveInfo[3]
                curveIdInfoFinder = re.compile("Curve ID Number: (\d*)$")

                contractionInfo = curveInfo[4]
                contractionInfoFinder = re.compile("\(edge\((v\d*), (v\d*)\), curve (\d*)\)")

                vertices = {}
                for m in vertexInfoFinder.finditer(vertexInfo):
                    if m:
                        vName = m.group(1)
                        vGenus = m.group(2)
                        v = vertex(vName, int(vGenus))
                        vertices[vName] = v

                edges = set()
                for m in edgeInfoFinder.finditer(edgeInfo):
                    if m:
                        eName = m.group(0)
                        eVert1Name = m.group(1)
                        eVert2Name = m.group(2)
                        e = edge(eName, 1.0, vertices[eVert1Name], vertices[eVert2Name])
                        edges.add(e)

                legs = set()
                for m in legInfoFinder.finditer(legInfo):
                    if m:
                        lName = m.group(0)
                        lRootName = m.group(1)
                        l = leg(lName, vertices[lRootName])
                        legs.add(l)

                c = CombCurve("")
                c.addEdges(edges)
                c.addLegs(legs)
                for vName in vertices:
                    c.addVertex(vertices[vName])

                self.curves.add(c)

                if c.edgeNumber in self.curvesDict:
                    self.curvesDict[c.edgeNumber].append(c)
                else:
                    self.curvesDict[c.edgeNumber] = [c]

                m = curveIdInfoFinder.match(curveIdInfo)
                if m:
                    curveId = m.group(1)
                    curveIdDictionary[curveId] = c

                edgeContractions = []
                for m in contractionInfoFinder.finditer(contractionInfo):
                    if m:
                        vert1 = vertices[m.group(1)]
                        vert2 = vertices[m.group(2)]
                        contractionID = m.group(3)
                        edgeContractions.append(({vert1, vert2}, contractionID))
                curveContractionDictionary[c] = edgeContractions
            for c in self.curves:
                self.contractionDict[c] = []
                edgeContractions = curveContractionDictionary[c]
                for e in c.edges:
                    contEntry = [entry for entry in edgeContractions if entry[0] == e.vertices].pop()
                    self.contractionDict[c].append((e, curveIdDictionary[contEntry[1]]))

    def saveModuliSpaceToFile(self, filename="", curveEntryDelimiter="=", encoding='utf-8'):
        if filename == "":
            filename = "SavedModuliSpaces/M-" + str(self._g) + "-" + str(self._n) + ".txt"

        with open(filename, mode='w', encoding=encoding) as f:
            curveNames = []
            for c in sorted(self.curves, key=lambda x: x.edgeNumber):
                c.simplifyNames()
                vertexNames = [("(" + v.name + " with genus " + str(v.genus) + ")") for v in c.vertices]
                edgeNames = [e.name for e in c.edges]
                legNames = [nextLeg.name for nextLeg in c.legs]
                vertexLine = "Vertices: {" + ",".join(vertexNames) + "}"
                edgeLine = "Edges: {" + ",".join(edgeNames) + "}"
                legLine = "Legs: {" + ",".join(legNames) + "}"
                curveNames.append("\n".join([vertexLine, edgeLine, legLine]))
            if curveNames:
                currentCurve = curveNames.pop()
                f.write(currentCurve)
                while curveNames:
                    currentCurve = curveNames.pop()
                    f.write("\n" + curveEntryDelimiter + "\n")
                    f.write(currentCurve)

    def saveSpaceAndContractions(self, filename="", curveEntryDelimiter="=", encoding='utf-8'):
        if filename == "":
            filename = "SavedModuliSpaces/M-" + str(self._g) + "-" + str(self._n) + ".txt"

        with open(filename, mode='w', encoding=encoding) as f:
            curveStrings = []
            curveList = sorted(self.curves, key=lambda x: x.edgeNumber)
            for c in curveList:
                c.simplifyNames()
                vertexNames = [("(" + v.name + " with genus " + str(v.genus) + ")") for v in c.vertices]
                edgeNames = [e.name for e in c.edges]
                legNames = [nextLeg.name for nextLeg in c.legs]
                vertexLine = "Vertices: {" + ",".join(vertexNames) + "}"
                edgeLine = "Edges: {" + ",".join(edgeNames) + "}"
                legLine = "Legs: {" + ",".join(legNames) + "}"
                idLine = "Curve ID Number: " + str(curveList.index(c))
                contractionLine = "Contraction info: "
                contractionStrings = []
                for info in self.contractionDict[c]:
                    contractionStrings.append("(" + info[1].name + ", curve " + str(curveList.index(info[0])) + ")")
                contractionLine += ", ".join(contractionStrings)
                curveStrings.append("\n".join([vertexLine, edgeLine, legLine, idLine, contractionLine]))
            if curveStrings:
                curveStrings.reverse()
                currentCurve = curveStrings.pop()
                f.write(currentCurve)
                while curveStrings:
                    currentCurve = curveStrings.pop()
                    f.write("\n" + curveEntryDelimiter + "\n")
                    f.write(currentCurve)
