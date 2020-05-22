import copy

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

#A leg has a name and root
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
        self._edges = set()
        self._legs = set()

        # Variables for caching vertices
        self._vertexCacheValid = False
        self._vertexCache = set()

        # Variables for caching genus
        self._genusCacheValid = False
        self._genusCache = 0

    @property
    def edges(self):
        return self._edges

    # Control how edges are set
    # edges_ should be a set of edges
    @edges.setter
    def edges(self, edges_):
        self._edges = edges_
        self._vertexCacheValid = False
        self._genusCacheValid = False

    @property
    def edgesWithVertices(self):
        return {e for e in self.edges if not (e.vert1 is None or e.vert2 is None)}

    @property
    def legs(self):
        return self._legs

    @property
    def legsWithVertices(self):
        return {leg for leg in self.legs if not leg.root is None}

    # Control how legs are set
    # legs_ should be a set of legs
    @legs.setter
    def legs(self, legs_):
        self._legs = legs_
        self._vertexCacheValid = False
        self._genusCacheValid = False
    
    # The set of vertices is a read only property computed upon access, unless a valid cache is available
    # It is the collection of vertices that are endpoints of edges or roots of legs
    @property
    def vertices(self):
        if not self._vertexCacheValid:
            # Flatmap self.edges with the function e => e.vertices
            unflattened_vertex_list = [e.vertices for e in self.edges] + [l.vertices for l in self.legs]
            flattened_vertex_list = []
            for sublist in unflattened_vertex_list:
                for vertex in sublist:
                    flattened_vertex_list.append(vertex)

            self._vertexCache = set(flattened_vertex_list) - {None}
            self._vertexCacheValid = True

        return self._vertexCache

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
        return sum(1 for e in self.edges if e.vert1 == v) + sum(1 for e in self.edges if e.vert2 == v) + sum(1 for l in self.legs if l.root == v)

    # e should be an edge and the length should be a double
    # genus should be a non-negative integer
    def subdivide(self, e, length, genus = 0):
        # Don't force a negative length
        assert 0.0 <= length and length <= e.length

        # Don't split a nonexistent edge
        assert e in self.edges

        v = vertex("(vertex splitting " + e.name + ")", genus)
        e1 = edge("(subdivision 1 of " + e.name + ")", length, e.vert1, v)
        e2 = edge("(subdivision 2 of " + e.name + ")", e.length - length, v, e.vert2)

        self.edges = self.edges - {e}
        self.edges = self.edges | {e1}
        self.edges = self.edges | {e2}

    # e should be an edge and the length should be a double
    # genus should be a non-negative integer
    # returns a new CombCurve with edge e subdivided
    def getSubdivision(self, e, length, genus = 0):
        subdivision = copy.copy(self)
        subdivision.subdivide(e, length, genus)
        return subdivision

    # v should be a vector
    # Returns the set of all elements of the form (e, n), where e is an edge, n is 1 or 2, and the n^th endpoint of e is v
    def getEndpointsOfEdges(self, v):
        endpoints = []
        for e in self.edges:
            if e.vert1 == v:
                endpoints += [(e, 1)]
            if e.vert2 == v:
                endpoints += [(e, 2)]
        for leg in self.legs:
            if leg.root == v:
                endpoints += [(leg, 1)]
        return set(endpoints)

    def getDegreeDict(self):
        degrees = {}
        for v in self.vertices:
            d = self.degree(v)
            if d in degrees:
                degrees[d] += 1
            else:
                degrees[d] = 1
        return degrees

    def getGenusDict(self):
        genuses = {}
        for v in self.vertices:
            g = v.genus
            if g in genuses:
                genuses[g] += 1
            else:
                genuses[g] = 1
        return genuses

    def getNumSelfLoops(self):
        return sum(1 for e in self.edges if len(e.vertices) == 1)

    def getVerticesByDegree(self):
        dict = {}
        for v in self.vertices:
            d = self.degree(v)
            if d in dict:
                dict[d].append(v)
            else:
                dict[d] = [v]
        return dict

    def getPermutations(self, lst):
        # If lst is empty then there are no permutations
        if len(lst) == 0:
            return []

            # If there is only one element in lst then, only
        # one permuatation is possible
        if len(lst) == 1:
            return [lst]

            # Find the permutations for lst if there are
        # more than 1 characters

        l = []  # empty list that will store current permutation

        # Iterate the input(lst) and calculate the permutation
        for i in range(len(lst)):
            m = lst[i]

            # Extract lst[i] or m from the list.  remLst is
            # remaining list
            remLst = lst[:i] + lst[i + 1:]

            # Generating all permutations where m is first
            # element
            for p in self.getPermutations(remLst):
                l.append([m] + p)
        return l

    def checkIfBijectionIsIsomorphism(self, other, domainOrderingDict, codomainOrderingDict):

        degreeList = list(domainOrderingDict.keys())

        inputList = []
        outputList = []
        for d in degreeList:
            inputList = inputList + domainOrderingDict[d]
            outputList = outputList + codomainOrderingDict[d]

        for i in range(len(inputList)):
            if inputList[i].genus != outputList[i].genus:
                return False
            numInputLegs = sum(1 for l in self.legs if l.root == inputList[i])
            numOutputLegs = sum(1 for l in other.legs if l.root == outputList[i])
            if numInputLegs != numOutputLegs:
                return False

        for i in range(len(inputList)):
            for j in range(len(inputList)):
                # Number of edges connecting inputList[i] and inputList[j]
                numInputEdges = sum(1 for e in self.edges if e.vertices == {inputList[i], inputList[j]})
                numOutputEdges = sum(1 for e in other.edges if e.vertices == [outputList[i], outputList[j]])
                if numInputEdges != numOutputEdges:
                    return False

        return True

    def getBijections(self, permDict):

        if len(permDict) == 0:
            return [{}]

        nextDegree = list(permDict.keys())[0]
        permsOfThatDegree = permDict.pop(nextDegree)
        remaining = self.getBijections(permDict)

        perms = []


        for perm in permsOfThatDegree:
            for subPerm in remaining:
                # Unioning dictionaries in python is next to impossible to do nicely :(
                newDict = {nextDegree: perm}
                for k in subPerm:
                    newDict[k] = subPerm[k]
                perms.append(newDict)
        return perms



    def isBruteForceIsomorphicTo(self, other):
        selfDegreeVertexDict = self.getVerticesByDegree()
        otherDegreeVertexDict = self.getVerticesByDegree()

        permDict = {}
        for d in selfDegreeVertexDict:
            permDict[d] = self.getPermutations(selfDegreeVertexDict[d])
        domainOrderingDicts = self.getBijections(permDict)

        for domainOrderingDict in domainOrderingDicts:
            if self.checkIfBijectionIsIsomorphism(other, domainOrderingDict, otherDegreeVertexDict):
                return True

        return False



    def isIsomorphicTo(self, other):
        if self.edgeNumber != other.edgeNumber:
            return False

        if self.vertexNumber != other.vertexNumber:
            return False

        deg1 = self.getDegreeDict()
        deg2 = other.getDegreeDict()
        if deg1 != deg2:
            return False

        gen1 = self.getGenusDict()
        gen2 = other.getGenusDict()
        if gen1 != gen2:
            return False

        loop1 = self.getNumSelfLoops()
        loop2 = other.getNumSelfLoops()
        if loop1 != loop2:
            return False

        return self.isBruteForceIsomorphicTo(other)



    def showNumbers(self):
        print("Number of Vertices: ", self.vertexNumber, " Number of Edges: ", self.edgeNumber)

    # Prints the names of vertices
    def showVertices(self):
        print([v.name for v in self.vertices])

    # Prints the names of edges
    def showEdges(self):
        print([e.name for e in self.edges])

    # Prints the names of legs
    def showLegs(self):
        print([l.name for l in self.legs])
