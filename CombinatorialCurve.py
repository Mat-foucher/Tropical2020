import copy
import numpy as np
from GraphIsoHelper import *
from RPC import *


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
    
    def __str__(self):
        return self.name + ", " + str(self._genus)

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
    # length_ should be a monoid element
    # vert1_ should be a vertex
    # vert2_ should be a vertex
    def __init__(self, name_, length_, vert1_, vert2_):
        self.name = name_
        self._length = length_

        # Distinguished endpoints to help identify self loops, and for other purposes
        self.vert1 = vert1_
        self.vert2 = vert2_

    @property
    def length(self):
        return self._length

    # Control how the length property is set
    # length_ should be a monoid element
    @length.setter
    def length(self, length_):
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
        self.monoid = Monoid()

        # Variables for caching vertices
        self._vertexCacheValid = False
        self._vertexCache = set()

        # Variables for caching genus
        self._genusCacheValid = False
        self._genusCache = 0

        # Variables for caching vertex characteristic counts
        self._vertexCharacteristicCacheValid = False
        self._vertexCharacteristicCache = {}

        # Variables for caching the core
        self._coreCacheValid = False
        self._coreCache = None

    def invalidateCaches(self):
        self._vertexCacheValid = False
        self._genusCacheValid = False
        self._vertexCharacteristicCacheValid = False
        self._coreCacheValid = False

    # The set of vertices is a read only property computed upon access, unless a valid cache is available
    # It is the collection of vertices that are endpoints of edges or roots of legs
    @property
    def vertices(self):
        return self._vertices

    def addVertex(self, v):
        if v is not None:
            self._vertices.add(v)

            # Possibly need to recalculate genus/core/etc.
            self.invalidateCaches()

    def addVertices(self, vertices):
        for v in copy.copy(vertices):
            self.addVertex(v)

    def removeVertex(self, v, removeDanglingVertices=False):
        if v in self._vertices:
            self._vertices.remove(v)

            # Removing a vertex removes all connected legs and edges
            for e in {e for e in self.edges if v in e.vertices}:
                self.removeEdge(e, removeDanglingVertices)
            for nextLeg in {nextLeg for nextLeg in self.legs if v in nextLeg.vertices}:
                self.removeLeg(nextLeg)

            # Possibly need to recalculate genus/core/etc.
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

        # Possibly need to recalculate genus/core/etc.
        self.invalidateCaches()

    def addEdges(self, edges):
        for e in copy.copy(edges):
            self.addEdge(e)

    def removeEdge(self, e, removeDanglingVertices=True):
        if e in self._edges:
            self._edges.remove(e)

            # A "dangling vertex" is an endpoint of e is isolated after we remove edge e
            # By default, removing an edge removes such vertices
            if removeDanglingVertices:
                for v in e.vertices:
                    if self.degree(v) == 0:
                        self.removeVertex(v)

            # Possibly need to recalculate genus/core/etc.
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

        # Possibly need to recalculate genus/core/etc.
        self.invalidateCaches()

    def addLeg(self, newLeg):
        self._legs.add(newLeg)
        self.addVertices(newLeg.vertices)

        # Possibly need to recalculate genus/core/etc.
        self.invalidateCaches()

    def addLegs(self, newLegs):
        for newLeg in copy.copy(newLegs):
            self.addLeg(newLeg)

    def removeLeg(self, badLeg, removeDanglingVertices=True):
        if badLeg in self._legs:
            self._legs.remove(badLeg)

            # The root of a leg is "dangling" if it becomes isolated after removing the leg
            # By default, removing a leg removes such a vertex
            if removeDanglingVertices:
                for v in badLeg.vertices:
                    if self.degree(v) == 0:
                        self.removeVertex(v)

            # Possibly need to recalculate genus/core/etc.
            self.invalidateCaches()

    def removeLegs(self, badLegs):
        for badLeg in copy.copy(badLegs):
            self.removeLeg(badLeg)

    @property
    def numVertices(self):
        return len(self.vertices)

    @property
    def numEdges(self):
        return len(self.edges)

    @property
    def numEdgesWithVertices(self):
        return len(self.edgesWithVertices)

    # The Betti number is a read only property computed upon access
    @property
    def bettiNumber(self):
        return self.numEdgesWithVertices - self.numVertices + 1

    @property
    def genus(self):
        # If the cached copy of genus is invalid, then recalculate it
        if not self._genusCacheValid:
            self._genusCache = self.bettiNumber + sum([v.genus for v in self.vertices])
            self._genusCacheValid = True
        return self._genusCache

    # Returns the degree of vertex v accounting for legs and self loops
    def degree(self, v):
        return self.edgeDegree(v) + self.legDegree(v)

    # Returns the number of endpoints of finite edges at vertex v
    def edgeDegree(self, v):
        return sum(1 for e in self.edges if e.vert1 == v) + sum(1 for e in self.edges if e.vert2 == v)

    # Returns the number of roots of legs at v
    def legDegree(self, v):
        return sum(1 for attachedLeg in self.legs if attachedLeg.root == v)

    # Returns a copy of this curve where all vertices, edges, and legs are also copied shallowly
    def getFullyShallowCopy(self, returnCopyInfo=False):
        # copyInfo will be a dictionary whose keys are the legs, edges, and vertices of self
        # copyInfo[*] will be the copy of *
        copyInfo = {}

        # First, copy the vertices of the graph and keep track of how it was done.
        # Even if the copy info is not returned, we need to know how vertices are copied to get compatible edge copies
        vertexCopyDict = {}
        for v in self.vertices:
            vCopy = copy.copy(v)
            vertexCopyDict[v] = vCopy

            if returnCopyInfo:
                copyInfo[v] = vCopy

        # Next, copy edges and legs
        edgeCopies = set()
        for nextEdge in self.edges:
            # Keep the same name and length, but use the new versions of endpoints
            nextEdgeCopy = edge(nextEdge.name, nextEdge.length,
                                vertexCopyDict[nextEdge.vert1], vertexCopyDict[nextEdge.vert2])
            edgeCopies.add(nextEdgeCopy)

            if returnCopyInfo:
                copyInfo[nextEdge] = nextEdgeCopy

        legCopies = set()
        for nextLeg in self.legs:
            # Keep the sane name, but use the new version of the root
            nextLegCopy = leg(nextLeg.name, vertexCopyDict[nextLeg.root])
            legCopies.add(nextLegCopy)

            if returnCopyInfo:
                copyInfo[nextLeg] = nextLegCopy

        # Build the copy
        curveCopy = CombCurve(self.name)
        curveCopy.addEdges(edgeCopies)
        curveCopy.addLegs(legCopies)

        if returnCopyInfo:
            return curveCopy, copyInfo
        else:
            return curveCopy

    # Contract edge e in place
    def contract(self, e):
        # Don't contract a nonexistent edge
        assert e in self.edges

        genus = 0
        if e.vert1 == e.vert2:
            # If e is a self loop, then the genus contribution of the loop will be placed in the new vertex
            genus = e.vert1.genus + 1
        else:
            # If e is not a self loop, then the new vertex only bears the genus of the endpoints
            genus = e.vert1.genus + e.vert2.genus

        v = vertex("(Contraction of " + e.name + ")", genus)

        # For each edge or leg adjacent to e, move endpoints to the contraction of e
        for nextEdge in copy.copy(self.edges) - {e}:
            if nextEdge.vert1 in e.vertices:
                nextEdge.vert1 = v
            if nextEdge.vert2 in e.vertices:
                nextEdge.vert2 = v
        for nextLeg in self.legs:
            if nextLeg.root in e.vertices:
                nextLeg.root = v

        # Apply the contraction
        self.addVertex(v)
        self.removeEdge(e)

    # Returns a new CombCurve with edge e contracted
    def getContraction(self, e, returnCopyInfo=False):
        # To avoid accidentally modifying self, we work with a fully shallow copy
        contraction, copyInfoDict = self.getFullyShallowCopy(True)

        # Safely contract the copy in place
        contraction.contract(copyInfoDict[e])

        if returnCopyInfo:
            return contraction, copyInfoDict
        else:
            return contraction

    # v should be a vertex
    # Returns the set of all elements of the form (e, n), where e is an edge or leg, n is 1 or 2,
    # and the n^th endpoint of e is v
    def getEndpointsOfEdges(self, v):

        endpoints = []

        for e in self.edges:
            if e.vert1 == v:
                endpoints += [(e, 1)]
            if e.vert2 == v:
                endpoints += [(e, 2)]

        # By default, consider the root of a leg to be its first endpoint
        for nextLeg in self.legs:
            if nextLeg.root == v:
                endpoints += [(nextLeg, 1)]

        return set(endpoints)

    # This dictionary keeps track of the number of vertices of a certain characteristic
    # Currently, the characteristic of a vertex v is a triple (d_e, d_l, g, l), where d_e is the edge degree of v,
    # d_l is the leg degree of v, and g is the genus of v, and there are l loops based at v.
    # The characteristic of a vertex is invariant under isomorphism, so if two graphs have different
    # "vertexEverythingDict"s, then they are definitely not isomorphic.
    @property
    def vertexCharacteristicCounts(self):
        # If the cached copy of the dictionary is invalid, then recalculate it.
        if not self._vertexCharacteristicCacheValid:
            self._vertexCharacteristicCache = {}
            for v in self.vertices:
                # Calculate the characteristic of v
                edgeDegree = self.edgeDegree(v)
                legDegree = self.legDegree(v)
                g = v.genus
                loops = sum(1 for e in self.edges if e.vertices == {v})
                key = (edgeDegree, legDegree, g, loops)

                # Increase the count of that characteristic, or set it to 1 if not already seen
                if key in self._vertexCharacteristicCache:
                    self._vertexCharacteristicCache[key] += 1
                else:
                    self._vertexCharacteristicCache[key] = 1

            self._vertexCharacteristicCacheValid = True

        return self._vertexCharacteristicCache

    # Very similar to the vertexCharacteristicCounts. Returns a dictionary vertexDict defined as follows. The keys of
    # vertexDict are triples of integers (d_e, d_l, g, l), and vertexDict[(d_e, d_l, g)] is the list of all vertices
    # with edge degree d_e, leg degree d_l, genus g, and l loops based at that vertex.
    # The values of vertexDict form a partition of self.vertices and every value of vertexDict is nonempty.
    # When brute-force checking for an isomorphism between two graphs, we only need to check bijections that preserve
    # corresponding characteristic blocks. (i.e., reduce the number of things to check from n! to
    # (n_1)! * (n_2)! * ... * (n_k)!, where n = n_1 + ... + n_k)
    def getVerticesByCharacteristic(self):
        vertexDict = {}
        for v in self.vertices:
            # Get the characteristic of v
            edgeDegree = self.edgeDegree(v)
            legDegree = self.legDegree(v)
            g = v.genus
            loops = sum(1 for e in self.edges if e.vertices == {v})
            key = (edgeDegree, legDegree, g, loops)

            # Update that characteristic entry, or initialize it if not already present
            if key in vertexDict:
                vertexDict[key].append(v)
            else:
                vertexDict[key] = [v]
        return vertexDict

    # Returns the number of edges whose endpoints are indistinct. Invariant under isomorphism
    def getNumSelfLoops(self):
        return sum(1 for e in self.edges if len(e.vertices) == 1)

    # Returns a list of all permutations of lst. A permutation of lst is itself a list.
    def getPermutations(self, lst):
        return GraphIsoHelper.getPermutations(lst)

    # Checks if the given data constitutes an isomorphism from self to other.
    # domainOrderingDict and codomainOrderingDict should have the same keys, and their values should partition the
    # vertices of self and other with all blocks of the partitions nonempty. The bijection f recovered from this data
    # is as follows: for each key k, and each index of domainOrderingDict[k],
    # f(domainOrderingDict[k][i]) = codomainOrderingDict[k][i].
    def checkIfBijectionIsIsomorphism(self, other, domainOrderingDict, codomainOrderingDict):
        return GraphIsoHelper.checkIfBijectionIsIsomorphism(self, other, domainOrderingDict, codomainOrderingDict)

    # permDict should be of type Dict[Any, List[List[Vertex]]]. It should have the property that for any choice function
    # f for the values of permDict, f(k_1) + ... + f(k_n) is a permutation of self.vertices, where k_1, ..., k_n are
    # the keys of permDict. Moreover, every permutation of self.vertices should arise in this manner.
    def getBijections(self, permDict):
        return GraphIsoHelper.getBijections(permDict)

    # Checks all bijections that preserve characteristic
    def isBruteForceIsomorphicTo(self, other):
        return GraphIsoHelper.isBruteForceIsomorphicTo(self, other)

    # Checks if some easy to check invariants are preserved, and then checks candidate bijections
    def isIsomorphicTo(self, other):
        return GraphIsoHelper.isIsomorphicTo(self, other)

    # Simplifies names of vertices, edges, and legs in place.
    def simplifyNames(self):
        orderedVertices = list(self.vertices)
        for i in range(len(orderedVertices)):
            orderedVertices[i].name = "v" + str(i)
        for e in self.edges:
            e.name = "edge(" + e.vert1.name + ", " + e.vert2.name + ")"
        for nextLeg in self.legs:
            nextLeg.name = "leg(" + nextLeg.root.name + ")"

    def showNumbers(self):
        print("Number of Vertices: ", self.numVertices, " Number of Edges: ", self.numEdges)

    @staticmethod
    def printCurve(curve):
        print("Vertices:")
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

        A = np.zeros((self.numVertices, self.numVertices))
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
                for k in range(self.numVertices):
                    if A[i][k] == 1:
                        if k not in numbers:
                            brandNewNumbers.append(k)

            newNumbers = []
            newNumbers.extend(brandNewNumbers)
            brandNewNumbers = []
            go = len(newNumbers) > 0

        return len(numbers) == self.numVertices



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

    # Class to assist in reasoning about loops and spanning trees
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
