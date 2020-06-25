from ..basic_families.BasicFamily import *
import re


class TropicalModuliSpace(object):
    def __init__(self, g_, n_):
        # Private copy of the genus and marking number of the space
        self._g = g_
        self._n = n_

        # Holds the strata of the space
        # Should not be set externally - the strata are generated based on _g and _n
        # The strata are not generated here since this can be a time-consuming process. (Let the user choose when to
        # take the time to do so...)
        self._curves = set()

        # Curves organized by number of edges
        self._curvesDict = {}

        # Dictionary tracking what each curve can contract to
        # contractionDict[curve]: List[(edge, Int)]
        # See the documentation for more explanation
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

    # Given input s of type Set[A], returns a list of all partitions of s into two subsets.
    # The return type of this function is List[(Set[A], Set[A]).
    def getPartitions(self, s):

        # An empty set has exactly one partition into two subsets
        if len(s) == 0:
            return [(set(), set())]

        # A singleton set has exactly two partitions into two subsets
        if len(s) == 1:
            elem = s.pop()
            s.add(elem)
            return [(set(), {elem}), ({elem}, set())]

        # If s has more than one element, then choose an arbitrary elem in s. Use recursion to produce the partitions
        # of s - {elem}, and then incorporate elem into these partitions.
        elem = s.pop()
        s.add(elem)
        p = self.getPartitions(s - {elem})

        partition = []
        for blockPair in p:
            # In order to incorporate elem into a partition (S, T) of s - {elem}, we can add elem to either S or T.
            S, T = blockPair
            partition.append((S | {elem}, T))
            partition.append((S, T | {elem}))

        return partition

    # Reduces the given list of curves by isomorphism.
    # If no curves are provided, then self.curves is modified in place,
    # and nothing is returned. This is to bring attention to the fact that this code has side-effects when no curves
    # are provided.
    # if returnReductionInformation is True, then some information about this reduction is returned. Specifically,
    # if P is a partition of curves into isotypes, then reductionDict is a right inverse (represented as a dictionary)
    # to some choice function over P.
    def reduceByIsomorphism(self, curves=None, returnReductionInformation=False):

        # If no curves are provided, then modify in place
        modifySelf = (curves is None)

        if modifySelf:
            # The curves are organized by their number of edges in curvesDict, so we can reduce each group
            # individually (this reduces the number of isomorphisms to check for).
            for n in self.curvesDict:
                self.curvesDict[n] = self.reduceByIsomorphism(self.curvesDict[n])

            # Now that curvesDict has been reduced, get the correct curves in self.curves.
            # Effectively, self.curves = union(self.curvesDict.values())
            self.curves = set()
            for n in self.curvesDict:
                self.curves = self.curves | set(self.curvesDict[n])
        else:
            # Since isomorphism is an equivalence relation, we might not have to check every pair of curves for iso.
            # Our algorithm is to iterate over the given curves and check for isomorphism with a representative of each
            # isotype.
            isotypes = []
            for curve in curves:
                # Until we check, assume that "curve" will represent a new isotype
                newIsotype = True

                # Actually perform the check
                for t in isotypes:
                    # If the curve isn't new, then add it to its isotype and stop checking
                    if t[0].isIsomorphicTo(curve):
                        t.append(curve)
                        newIsotype = False
                        break

                # If we made it here without unsetting the newIsotype flag, then the curve represents a new isotype.
                if newIsotype:
                    isotypes.append([curve])

            if returnReductionInformation:
                reductionDict = {t[0]: t for t in isotypes}
                return {t[0] for t in isotypes}, reductionDict
            else:
                return {t[0] for t in isotypes}

    # Checks if curve is contained in self.curves up to isomorphism.
    # Optionally, the user can ask for the match to be returned, if it exists.
    def containsUpToIsomorphism(self, curve, returnMatch=False):

        # We only need to compare against curves with the same number of edges
        if curve.numEdges not in self.curvesDict:
            if returnMatch:
                return False, None
            else:
                return False
        else:
            # Check for isomorphism with curves of the same number of edges
            for c in self.curvesDict[curve.numEdges]:
                if c.isIsomorphicTo(curve):
                    if returnMatch:
                        return True, c
                    else:
                        return True

        # If this code is reached, then no match was found
        if returnMatch:
            return False, None
        else:
            return False

    # Adds "curve" to self.curves and self.curvesDict if it is not already present up to isomorphism. If the curve is
    # already present, then nothing is added.
    def addCurve(self, curve):

        curveIsNew = not self.containsUpToIsomorphism(curve)

        if curveIsNew:
            numEdges = curve.numEdges

            # Decide whether we need to initialize or update self.curvesDict[numEdges]
            if numEdges in self.curvesDict:
                self.curvesDict[numEdges] = self.curvesDict[numEdges] + [curve]
            else:
                self.curvesDict[numEdges] = [curve]

            # Update self.curves
            self.curves = self.curves | {curve}

    # Adds the specializations of curve to self.curves
    def addSpecializationsDFS(self, curve):
        newCurves = []

        # Get the one-step specializations of the given curve
        for vert in curve.vertices:

            # If the genus of vert is greater than 1, then we can decrement its genus and add a self loop
            if vert.genus > 1:
                genusReducedCurve = self.getGenusReductionSpecialization(curve, vert)
                newCurves.append(genusReducedCurve)
            # If the genus of vert is exactly 1, we need to make sure that stability is preserved after genus reduction
            # This case should only occur when g=1 and we process the seed curve
            elif vert.genus == 1 and curve.degree(vert) > 0:
                genusReducedCurve = self.getGenusReductionSpecialization(curve, vert)
                newCurves.append(genusReducedCurve)

            # We can also split a vertex in two and pass around parts of its genus and endpoints to the new pieces
            endpointPartitions = self.getPartitions(curve.getEndpointsOfEdges(vert))

            # Anticipate some isomorphic results - (S, T) and (T, S) produce the same splitting specialization
            endpointPartitions = [(S, T) for (S, T) in endpointPartitions if len(S) <= len(T)]

            # Iterate over the possible genuses of the split vertices
            for g in range(vert.genus + 1):
                for p in endpointPartitions:
                    S, T = p
                    # Make sure that the splitting specialization will be stable
                    if not ((g == 0 and len(S) < 2) or (g == vert.genus and len(T) < 2)):
                        vertexSplitCurve = self.getSplittingSpecialization(curve, vert, g, vert.genus - g, S, T)
                        newCurves.append(vertexSplitCurve)

        # Reduce newCurves before we go down a level - produce fewer curves to reduce in the future
        newCurvesBuffer = self.reduceByIsomorphism(newCurves)
        newCurves = []
        for c in newCurvesBuffer:
            if not self.containsUpToIsomorphism(c):
                newCurves.append(c)
                self.addCurve(c)

        #print("Found ", len(newCurves), " new curves")
        #print("Currently have ", len(self.curves), " curves!")

        # Specialize the specializations DFS - Moduli Spaces have a wide DAG structure (under the contraction relation)
        for c in newCurves:
            self.addSpecializationsDFS(c)

    # Generates M_{g, n}. To do so, start with the unique n-marked curve of genus g without any edges, and add its
    # specializations.
    def generateSpaceDFS(self):

        # start_time = time.time()

        # Manually check to see if the space is empty.
        if self._g == 0 and self._n < 3:
            return

        # If the space is nonempty, then all of the curves are specializations of seedCurve
        seedCurve = BasicFamily("Seed curve with genus " + str(self._g) + ", " + str(self._n) + " legs, and 0 edges")
        v = Vertex("v", self._g)
        seedCurve.addVertex(v)
        seedCurve.addLegs({Leg("leg " + str(i), v) for i in range(self._n)})
        seedCurve.monoid = Monoid()

        # Let the seed grow!
        self.addCurve(seedCurve)
        self.addSpecializationsDFS(seedCurve)

        # generation_complete_time = time.time()

        # print("Generation time: ", generation_complete_time - start_time)

    # For each curve in the space, and each edge of the curve, identify what curve in the space is isomorphic to the
    # contraction by that edge.
    def generateContractionDictionary(self):
        # At this point, the strata should have been generated, so we can nicely print out progress
        numCurves = len(self.curves)
        it = 1

        # Find contraction info of every curve
        for curve in self.curves:
            print("Working on getting contraction history of curve", str(it) + "/" + str(numCurves),
                  "of M-" + str(self._g) + "-" + str(self._n))

            # Find each contraction pair (curve/{e}, e)
            contractionPairs = []
            for nextEdge in curve.edges:
                contractionCurve = curve.getContraction(nextEdge)

                # Find curve/{e} up to isomorphism
                p = self.containsUpToIsomorphism(contractionCurve, returnMatch=True)
                containsAMatch = p[0]
                match = p[1]

                # This had better be true! Remember to generate the space...
                assert containsAMatch
                contractionPairs.append((nextEdge, match))

            self.contractionDict[curve] = contractionPairs
            it += 1

    # Specializes 'curve' at 'vert' as determined by g1, g2, S, and T
    # Specifically, 'vert' is split into two vertices, v1 and v2, of genuses g1 and g2 respectively,
    # where g1+g2 == vert.genus
    # S and T partition the endpoints of edges on vert, and we move the endpoints of edges in S to v1 and those
    # in T to v2
    @staticmethod
    def specializeBySplittingAtVertex(curve, vert, g1, g2, S, T):
        assert g1 + g2 == vert.genus
        v1 = Vertex("(First split of " + vert.name + ")", g1)
        v2 = Vertex("(Second split of " + vert.name + ")", g2)

        for p in S:
            e, edgeNum = p
            if isinstance(e, Edge):
                if edgeNum == 1:
                    e.vert1 = v1
                else:
                    e.vert2 = v1
            else:
                e.root = v1

        for p in T:
            e, edgeNum = p
            if isinstance(e, Edge):
                if edgeNum == 1:
                    e.vert1 = v2
                else:
                    e.vert2 = v2
            else:
                e.root = v2

        curve.monoid.addgen("(Edge splitting " + vert.name + ")")
        newLength = curve.monoid.Element({"(Edge splitting " + vert.name + ")": 1})
        e = Edge("(Edge splitting " + vert.name + ")", newLength, v1, v2)

        curve.addEdge(e)
        curve.removeVertex(vert)

    # Returns the splitting specialization of curve as determined by the other inputs
    def getSplittingSpecialization(self, curve, vert, g1, g2, S, T):
        # copy the curve shallowly and keep track of how copying was performed
        # This will allow us to split without worrying about affecting self
        c, copyInfo = curve.getFullyShallowCopy(True)
        c.name = "(Spec. of " + curve.name + " from splitting at " + vert.name

        # Also grab a safe copy of S and T
        safeS = {(copyInfo[e], n) for (e, n) in S}
        safeT = {(copyInfo[e], n) for (e, n) in T}

        # Specialize our copy in-place
        self.specializeBySplittingAtVertex(c, copyInfo[vert], g1, g2, safeS, safeT)

        return c

    @staticmethod
    def specializeByReducingGenus(curve, vert):
        assert vert.genus > 0

        endpoints = curve.getEndpointsOfEdges(vert)

        v = Vertex("(Genus reduction of " + vert.name + ")", vert.genus - 1)

        for p in endpoints:
            e, edgeNum = p
            if isinstance(e, Edge):
                if edgeNum == 1:
                    e.vert1 = v
                else:
                    e.vert2 = v
            else:
                e.root = v

        curve.monoid.addgen("(Genus reduction loop for " + vert.name + ")")
        newLength = curve.monoid.Element({"(Genus reduction loop for " + vert.name + ")": 1})
        e = Edge("(Genus reduction loop for " + vert.name + ")", newLength, v, v)

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

                c = BasicFamily("")
                c.monoid = Monoid()

                vertices = {}
                for m in vertexInfoFinder.finditer(vertexInfo):
                    if m:
                        vName = m.group(1)
                        vGenus = m.group(2)
                        v = Vertex(vName, int(vGenus))
                        vertices[vName] = v

                edges = set()
                for m in edgeInfoFinder.finditer(edgeInfo):
                    if m:
                        eName = m.group(0)
                        eVert1Name = m.group(1)
                        eVert2Name = m.group(2)

                        c.monoid.addgen(eName)
                        eLength = c.monoid.Element({eName: 1})

                        e = Edge(eName, eLength, vertices[eVert1Name], vertices[eVert2Name])
                        edges.add(e)

                legs = set()
                for m in legInfoFinder.finditer(legInfo):
                    if m:
                        lName = m.group(0)
                        lRootName = m.group(1)
                        legs.add(Leg(lName, vertices[lRootName]))

                c.addEdges(edges)
                c.addLegs(legs)
                for vName in vertices:
                    c.addVertex(vertices[vName])

                self.curves.add(c)

                if c.numEdges in self.curvesDict:
                    self.curvesDict[c.numEdges].append(c)
                else:
                    self.curvesDict[c.numEdges] = [c]

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
            curveStrings = []
            curveList = sorted(self.curves, key=lambda x: x.numEdges)
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
