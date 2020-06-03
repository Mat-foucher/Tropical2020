import copy
import numpy as np
from GraphIsoHelper import *


# A vertex has a name and non-negative genus
class vertex(object):
    # name_ should be a string identifier - only unique if the user is careful (or lucky) to make it so
    # genus_ should be a non-negative integer
    def __init__(self, name_, genus_):
        # Don't allow negative genus!
        if genus_ < 0:
            raise ValueError("Genus must be non-negative")
        self.name = name_
        self._genus = genus_

    @property
    def genus(self):
        return self._genus

    # Control how the genus property is set
    # genus_ should be a non-negative integer
    @genus.setter
    def genus(self, genus_):
        # Don't allow negative genus!
        if genus_ < 0:
            raise ValueError("Genus must be non-negative.")
        self._genus = genus_


# An edge has a name, non-negative length, and endpoints
class edge(object):
    # name_ should be a string identifier - only unique if the user is careful (or lucky) to make it so
    # length_ should be a non-negative double
    # vert1_ should be a vertex
    # vert2_ should be a vertex
    def __init__(self, name_, length_, vert1_, vert2_):
        self.name = name_

        # Don't allow negative lengths!
        if length_ < 0.0:
            raise ValueError("Length must be non-negative.")
        self._length = length_

        # Distinguished endpoints to help identify self loops
        self.vert1 = vert1_
        self.vert2 = vert2_

    @property
    def length(self):
        return self._length

    # Control how the length property is set
    # length_ should be a non-negative double
    @length.setter
    def length(self, length_):
        # Don't allow negative lengths!
        if length_ < 0.0:
            raise ValueError("Length must be non-negative.")
        self._length = length_

    # The set of vertices is a read only property computed upon access
    @property
    def vertices(self):
        return {self.vert1, self.vert2}


# A leg has a name and root
class leg(object):
    # name_ should be a string identifier - only unique if the user is careful (or lucky) to make it so
    # root_ should be a vertex
    def __init__(self, name_, root_):
        self.name = name_
        self.root = root_

    # The set of vertices is a read only property computed upon access
    @property
    def vertices(self):
        return {self.root}


# A Combinatorial Tropical Curve has a name, set of edges, and set of legs
class CombCurve(object):
    # name_ should be a string identifier - only unique if the user is careful (or lucky) to make it so
    def __init__(self, name_):
        self.name = name_
        self._vertices = set()
        self._edges = set()
        self._legs = set()

        # Variables for caching vertices
        self._vertexCacheValid = False
        self._vertexCache = set()

        # Variables for caching genus
        self._genusCacheValid = False
        self._genusCache = 0

        # Variables for caching vertex self loop counts
        self._vertexSelfLoopsCacheValid = False
        self._vertexSelfLoopsCache = {}

        # Variables for caching vertex everything couns
        self._vertexEverythingCacheValid = False
        self._vertexEverythingCache = {}

        # Variables for caching the core
        self._coreCacheValid = False
        self._coreCache = None

    def invalidateCaches(self):
        self._vertexCacheValid = False
        self._genusCacheValid = False
        self._vertexSelfLoopsCacheValid = False
        self._vertexEverythingCacheValid = False
        self._coreCacheValid = False

    # The set of vertices is a read only property computed upon access, unless a valid cache is available
    # It is the collection of vertices that are endpoints of edges or roots of legs
    @property
    def vertices(self):
        return self._vertices

    def addVertex(self, v):
        if v is not None:
            self._vertices.add(v)
            self.invalidateCaches()

    def addVertices(self, vertices):
        for v in copy.copy(vertices):
            self.addVertex(v)

    def removeVertex(self, v, removeDanglingVertices=False):
        if v in self._vertices:
            self._vertices.remove(v)
            for e in {e for e in self.edges if v in e.vertices}:
                self.removeEdge(e, removeDanglingVertices)
            for nextLeg in {nextLeg for nextLeg in self.legs if v in nextLeg.vertices}:
                self.removeLeg(nextLeg)
            self.invalidateCaches()

    def removeVertices(self, vertices):
        for v in copy.copy(vertices):
            self.removeVertex(v)

    @property
    def edges(self):
        return self._edges

    @property
    def edgesWithVertices(self):
        return {e for e in self.edges if not (e.vert1 is None or e.vert2 is None)}

    # Control how edges are set
    # edges_ should be a set of edges
    @edges.setter
    def edges(self, edges_):
        self._edges = edges_
        self.invalidateCaches()

    def addEdge(self, e):
        self._edges.add(e)
        self.addVertices(e.vertices)
        self.invalidateCaches()

    def addEdges(self, edges):
        for e in copy.copy(edges):
            self.addEdge(e)

    def removeEdge(self, e, removeDanglingVertices=True):
        if e in self._edges:
            self._edges.remove(e)
            if removeDanglingVertices:
                for v in e.vertices:
                    if self.degree(v) == 0:
                        self.removeVertex(v)
            self.invalidateCaches()

    def removeEdges(self, edges):
        for e in copy.copy(edges):
            self.removeEdge(e)

    @property
    def legs(self):
        return self._legs

    @property
    def legsWithVertices(self):
        return {nextLeg for nextLeg in self.legs if nextLeg.root is not None}

    # Control how legs are set
    # legs_ should be a set of legs
    @legs.setter
    def legs(self, legs_):
        self._legs = legs_
        self.invalidateCaches()

    def addLeg(self, newLeg):
        self._legs.add(newLeg)
        self.addVertices(newLeg.vertices)
        self.invalidateCaches()

    def addLegs(self, newLegs):
        for newLeg in copy.copy(newLegs):
            self.addLeg(newLeg)

    def removeLeg(self, badLeg, removeDanglingVertices=True):
        if badLeg in self._legs:
            self._legs.remove(badLeg)
            if removeDanglingVertices:
                for v in badLeg.vertices:
                    if self.degree(v) == 0:
                        self.removeVertex(v)
            self.invalidateCaches()

    def removeLegs(self, badLegs):
        for badLeg in copy.copy(badLegs):
            self.removeLeg(badLeg)

    # The number of vertices is a read only property computed upon access
    # It is the number of vertices
    @property
    def vertexNumber(self):
        return len(self.vertices)

    # The number of edges is a read only property computed upon access
    # It is the number of edges
    @property
    def edgeNumber(self):
        return len(self.edges)

    @property
    def numEdgesWithVertices(self):
        return len(self.edgesWithVertices)

    # The Betti number is a read only property computed upon access
    @property
    def bettiNumber(self):
        return self.numEdgesWithVertices - self.vertexNumber + 1

    # Genus is a read only property computed upon access
    @property
    def genus(self):
        if not self._genusCacheValid:
            self._genusCache = self.bettiNumber + sum([v.genus for v in self.vertices])
            self._genusCacheValid = True
        return self._genusCache

    # Returns the degree of vertex v accounting for legs and self loops
    def degree(self, v):
        return self.edgeDegree(v) + self.legDegree(v)

    def edgeDegree(self, v):
        return sum(1 for e in self.edges if e.vert1 == v) + sum(1 for e in self.edges if e.vert2 == v)

    def legDegree(self, v):
        return sum(1 for attachedLeg in self.legs if attachedLeg.root == v)

    # Returns a copy of this curve where all vertices, edges, and legs are also copied shallowly
    def getFullyShallowCopy(self, returnCopyInfo=False):
        copyInfo = {}
        vertexCopyDict = {}
        for v in self.vertices:
            vCopy = copy.copy(v)
            vertexCopyDict[v] = vCopy

            if returnCopyInfo:
                copyInfo[v] = vCopy

        edgeCopies = set()
        legCopies = set()
        for nextEdge in self.edges:
            nextEdgeCopy = edge(nextEdge.name, nextEdge.length,
                                vertexCopyDict[nextEdge.vert1], vertexCopyDict[nextEdge.vert2])
            edgeCopies.add(nextEdgeCopy)

            if returnCopyInfo:
                copyInfo[nextEdge] = nextEdgeCopy

        for nextLeg in self.legs:
            nextLegCopy = leg(nextLeg.name, vertexCopyDict[nextLeg.root])
            legCopies.add(nextLegCopy)

            if returnCopyInfo:
                copyInfo[nextLeg] = nextLegCopy

        curveCopy = CombCurve(self.name)
        curveCopy.addEdges(edgeCopies)
        curveCopy.addLegs(legCopies)

        if returnCopyInfo:
            return curveCopy, copyInfo
        else:
            return curveCopy

    # e should be an edge and the length should be a double
    # genus should be a non-negative integer
    def subdivide(self, e, length, genus=0):
        # Don't force a negative length
        assert 0.0 <= length <= e.length

        # Don't split a nonexistent edge
        assert e in self.edges

        v = vertex("(vertex splitting " + e.name + ")", genus)
        e1 = edge("(subdivision 1 of " + e.name + ")", length, e.vert1, v)
        e2 = edge("(subdivision 2 of " + e.name + ")", e.length - length, v, e.vert2)

        self.removeEdge(e)
        self.addEdges({e1, e2})

    # e should be an edge and the length should be a double
    # genus should be a non-negative integer
    # returns a new CombCurve with edge e subdivided
    def getSubdivision(self, e, length, returnCopyInfo=False, genus=0):
        subdivision, copyInfoDict = self.getFullyShallowCopy(True)
        subdivision.subdivide(copyInfoDict[e], length, genus)
        if returnCopyInfo:
            return subdivision, copyInfoDict
        else:
            return subdivision

    # v should be a vector
    # Returns the set of all elements of the form (e, n), where e is an edge, n is 1 or 2,
    # and the n^th endpoint of e is v
    def getEndpointsOfEdges(self, v):
        endpoints = []
        for e in self.edges:
            if e.vert1 == v:
                endpoints += [(e, 1)]
            if e.vert2 == v:
                endpoints += [(e, 2)]
        for nextLeg in self.legs:
            if nextLeg.root == v:
                endpoints += [(nextLeg, 1)]
        return set(endpoints)

    @property
    def vertexEverythingDict(self):
        if not self._vertexEverythingCacheValid:
            self._vertexEverythingCache = {}
            for v in self.vertices:
                edgeDegree = self.edgeDegree(v)
                legDegree = self.legDegree(v)
                g = v.genus
                key = (edgeDegree, legDegree, g)
                if key in self._vertexEverythingCache:
                    self._vertexEverythingCache[key] += 1
                else:
                    self._vertexEverythingCache[key] = 1

            self._vertexEverythingCacheValid = True
        return self._vertexEverythingCache

    def getVerticesByEverything(self):
        vertexDict = {}
        for v in self.vertices:
            edgeDegree = self.edgeDegree(v)
            legDegree = self.legDegree(v)
            g = v.genus
            key = (edgeDegree, legDegree, g)
            if key in vertexDict:
                vertexDict[key].append(v)
            else:
                vertexDict[key] = [v]
        return vertexDict

    def getNumSelfLoops(self):
        return sum(1 for e in self.edges if len(e.vertices) == 1)

    @property
    def vertexSelfLoopDict(self):
        if not self._vertexSelfLoopsCacheValid:
            self._vertexSelfLoopsCache = {}
            for v in self.vertices:
                numLoops = sum(1 for e in self.edges if e.vertices == {v})
                if numLoops in self._vertexSelfLoopsCache:
                    self._vertexSelfLoopsCache[numLoops] += 1
                else:
                    self._vertexSelfLoopsCache[numLoops] = 1
            self._vertexSelfLoopsCacheValid = True
        return self._vertexSelfLoopsCache

    def getPermutations(self, lst):
        return GraphIsoHelper.getPermutations(lst)

    def checkIfBijectionIsIsomorphism(self, other, domainOrderingDict, codomainOrderingDict):
        return GraphIsoHelper.checkIfBijectionIsIsomorphism(self, other, domainOrderingDict, codomainOrderingDict)

    def getBijections(self, permDict):
        return GraphIsoHelper.getBijections(permDict)

    def isBruteForceIsomorphicTo(self, other):
        return GraphIsoHelper.isBruteForceIsomorphicTo(self, other)

    def isIsomorphicTo(self, other):
        return GraphIsoHelper.isIsomorphicTo(self, other)

    def simplifyNames(self):
        orderedVertices = list(self.vertices)
        for i in range(len(orderedVertices)):
            orderedVertices[i].name = "v" + str(i)
        for e in self.edges:
            e.name = "edge(" + e.vert1.name + ", " + e.vert2.name + ")"
        for nextLeg in self.legs:
            nextLeg.name = "leg(" + nextLeg.root.name + ")"

    def showNumbers(self):
        print("Number of Vertices: ", self.vertexNumber, " Number of Edges: ", self.edgeNumber)

    @staticmethod
    def printCurve(curve):
        print("\n\nVertices:")
        for v in curve.vertices:
            print(v.name, " with genus ", v.genus)
        print("Edges:")
        for e in curve.edges:
            print(e.name)
        print("Legs:")
        for nextLeg in curve.legs:
            print(nextLeg.name)

    def printSelf(self):
        CombCurve.printCurve(self)

    # Prints the names of vertices
    def showVertices(self):
        print([v.name for v in self.vertices])

    # Prints the names of edges
    def showEdges(self):
        print([e.name for e in self.edges])

    # Prints the names of legs
    def showLegs(self):
        print([nextLeg.name for nextLeg in self.legs])

    # This function will check if the tropical curve is connected (in the style of Def 3.10)
    @property
    def isConnected(self):

        A = np.zeros((self.vertexNumber, self.vertexNumber))
        _vertices = list(self.vertices)

        for x in self.edges:
            v1 = x.vert1
            v2 = x.vert2

            i = _vertices.index(v1)
            j = _vertices.index(v2)

            # print(i, j)
            # So that the connections made by the edges are symmetric ((v1,v2) = (v2,v1))
            A[i][j] = 1
            A[j][i] = 1

        # So that the while loop works
        go = True
        numbers = []
        newNumbers = [0]

        while go:
            numbers.extend(newNumbers)
            brandNewNumbers = []
            for i in newNumbers:
                for k in range(self.vertexNumber):
                    if A[i][k] == 1:
                        if k not in numbers:
                            brandNewNumbers.append(k)

            newNumbers = []
            newNumbers.extend(brandNewNumbers)
            brandNewNumbers = []
            go = len(newNumbers) > 0

        return len(numbers) == self.vertexNumber



    @property
    def core(self):

        # Calculate the core if our current copy is invalid
        if not self._coreCacheValid:

            # Only allow the core to be requested from curves where the core is defined.
            if not self.genus > 0:
                raise ValueError("The core is only defined for curves of positive genus.")
            if not self.isConnected:
                raise ValueError("The core is only defined for connected curves.")

            # In order to generate the core, we start with a copy of self and repeatedly prune off certain leaves
            core = CombCurve("(Core of " + self.name + ")")
            core.addEdges(self.edges)
            core.addVertices(self.vertices)

            # Flag to indicate whether new leaves were pruned
            keepChecking = True

            while keepChecking:

                # If nothing happens this loop, then stop.
                keepChecking = False

                # Search for leaves to prune
                for nextVertex in copy.copy(core.vertices):
                    # A vertex is the endpoint of a leaf to prune if it is connected to exactly one edge and has
                    # genus zero
                    if nextVertex.genus == 0 and core.degree(nextVertex) < 2:
                        # Prune the leaf
                        core.removeVertex(nextVertex)
                        keepChecking = True

            # Save the new, valid, core and set the valid flag to true
            self._coreCache = core
            self._coreCacheValid = True

        # Return the saved copy of the core (possibly just calculated)
        return self._coreCache

    class Tree:
        def __init__(self):
            # Tree Parent
            self.parent = None
            # Edge connecting self to parent
            self.parentConnection = None
            # Node holds a vertex value
            self.value = None
            # List of (Tree, Edge) children
            self.children = []

        def setValue(self, vert):
            self.value = vert

        def setParent(self, p):
            self.parent = p

        def addChild(self, vert, connectingEdge):
            if (
                    # Don't allow a self loop to be added
                    (vert != self.value) and
                    # Make sure connectingEdge is actually a connecting edge
                    (connectingEdge.vertices == {self.value, vert}) and
                    # Don't introduce any loops
                    (vert not in self.getVertices())
            ):
                childTree = CombCurve.Tree()
                childTree.setValue(vert)
                childTree.setParent(self)
                childTree.parentConnection = connectingEdge
                self.children.append((childTree, connectingEdge))

        def getEdgesOfChildren(self):
            edges = []
            for child in self.children:
                childTree, connectingEdge = child
                edges.append(connectingEdge)
                edges += childTree.getEdgesOfChildren()
            return edges

        def getEdges(self):
            # If we're actually the root of the whole tree, then descend recursively
            if self.parent is None:
                return self.getEdgesOfChildren()
            else:
                return self.parent.getEdges()

        def getVerticesFromChildren(self):
            vertices = {self.value}
            for child in self.children:
                childTree, connectingEdge = child
                vertices = vertices | childTree.getVerticesFromChildren()
            return vertices

        def getVertices(self):
            if self.parent is None:
                return self.getVerticesFromChildren()
            else:
                return self.parent.getVertices()

        def findVertexInChildren(self, vert):
            if self.value == vert:
                return self
            else:
                for child in self.children:
                    childTree, connectingEdge = child
                    possibleFind = childTree.findVertexInChildren(vert)
                    if possibleFind is not None:
                        return possibleFind
                return None

        def findVertex(self, vert):
            if self.parent is None:
                return self.findVertexInChildren(vert)
            else:
                return self.parent.findVertex(vert)

        def getAncestorEdges(self, vert):
            currentTree = self.findVertex(vert)
            ancestorEdges = []

            while currentTree.parent is not None:
                ancestorEdges.append(currentTree.parentConnection)
                currentTree = currentTree.parent

            return ancestorEdges



    @property
    def spanningTree(self):
        return self.getSpanningTree(list(self.vertices)[0])

    # Will return a list of edges in a loop.
    def getLoop(self, e):
        spanningTree = self.spanningTree
        if e in spanningTree.getEdges():
            raise ValueError("Edge " + e.name + " must not belong to the spanning tree to determine a unique loop.")

        anc1 = spanningTree.getAncestorEdges(e.vert1)
        anc2 = spanningTree.getAncestorEdges(e.vert2)

        leastAncestorIndex = 0
        for i in range(min(len(anc1), len(anc2))):
            leastAncestorIndex = i
            if anc1[i] != anc2[i]:
                break
        else:
            leastAncestorIndex = min(len(anc1), len(anc2))

        anc1 = anc1[leastAncestorIndex:]
        anc2 = anc2[leastAncestorIndex:]
        anc1.reverse()

        if anc1 == [None]:
            anc1 = []

        if anc2 == [None]:
            anc2 = []

        return anc1 + [e] + anc2

    # Returns a list of lists of edges.
    @property
    def loops(self):
        loopDeterminers = self.edges - set(self.spanningTree.getEdges())
        _loops = []
        for nextEdge in loopDeterminers:
            _loops.append(self.getLoop(nextEdge))
        return _loops

    def getSpanningTree(self, vert):
        
        if not self.isConnected:
            raise ValueError("A spanning tree is only defined for a connected graph")

        tree = self.Tree()          
        tree.setValue(vert)

        verticesToCheck = {vert}

        while len(verticesToCheck) > 0:

            nextVertex = verticesToCheck.pop()

            connectedEdges = {e for e in self.edges if (nextVertex == e.vert1 or nextVertex == e.vert2)} 

            adjacentVertices = set()          

            for e in connectedEdges:
                adjacentVertices = adjacentVertices | e.vertices 

            newAdjacentVertices = adjacentVertices - set(tree.getVertices())

            nextTree = tree.findVertex(nextVertex)    

            for v in newAdjacentVertices:
                connectingEdge = {e for e in self.edges if e.vertices == {nextVertex, v}}.pop()
                nextTree.addChild(v, connectingEdge)

            verticesToCheck = verticesToCheck | newAdjacentVertices

        return tree
