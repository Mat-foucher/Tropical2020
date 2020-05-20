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
    def setLength(self, length_):
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
        self._edges = {}
        self._legs = {}

        # Variables for caching vertices
        self._vertexCacheValid = False
        self._vertexCache = {}

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
    def legs(self):
        return self._legs

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

            self._vertexCache = set(flattened_vertex_list)
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



    # The Betti number is a read only property computed upon access
    @property
    def bettiNumber(self):
        return self.edgeNumber - self.vertexNumber + 1

    # Genus is a read only property computed upon access
    @property
    def genus(self):
        if not self._genusCacheValid:
            self._genusCahce = self.bettiNumber + sum([v.genus for v in self.vertices])
            self._genusCacheValid = True
        return self.bettiNumber + sum([v.genus for v in self.vertices])



    # Returns the degree of vertex v accounting for legs and self loops
    def degree(self, v):
        return sum(1 for e in self.edges if e.vert1 == v) + sum(1 for e in self.edges if e.vert2 == v) + sum(1 for l in self.legs if l.root == v)

    # e should be an edge and the lengths should be doubles
    # genus should be a non-negative integer
    # returns a new CombCurve with edge e subdivided
    def getSubdivision(self, e, length1, length2, genus = 0):
        # Ensure the lengths are non-negative
        if length1 < 0.0:
            raise ValueError("length1 must be non-negative")
        if length2 < 0.0:
            raise ValueError("length2 must be non-negative")

        # Ensure the lengths sum to the length of e
        assert length1 + length2 == e.length

        # Don't split a nonexistent edge
        assert e in self.edges

        v = vertex("(vertex splitting " + e.name + ")", genus)
        e1 = edge("(subdivision 1 of " + e.name + ")", length1, e.vert1, v)
        e2 = edge("(subdivision 2 of " + e.name + ")", length2, v, e.vert2)

        subdivision = copy.copy(self)

        subdivision.edges = subdivision.edges - {e}
        subdivision.edges = subdivision.edges | {e1}
        subdivision.edges = subdivision.edges | {e2}

        return subdivision



    def showNumbers(self):
        print "Number of Vertices: ", self.vertexNumber, " Number of Edges: ", self.edgeNumber

    # Prints the names of vertices
    def showVertices(self):
        print [v.name for v in self.vertices]

    # Prints the names of edges
    def showEdges(self):
        print [e.name for e in self.edges]

    # Prints the names of legs
    def showLegs(self):
        print [l.name for l in self.legs]


class StrictPiecewiseLinearFunction(object):
    # domain_ should be a CombCurve representing the domain of the function
    # functionValues_ should be a dictionary with vertex/leg keys and non-negative double values
    def __init__(self, domain_, functionValues_):
        self._domain = domain_
        self._functionValues = functionValues_
        self.assertIsAffineLinear()

    # Make the domain read only
    @property
    def domain(self):
        return self._domain 

    # Make the function read only
    @property
    def functionValues(self):
        return self._functionValues

    def assertIsAffineLinear(self):
        # Assert Non-Negativity at every iteration of the loop!
        for i in self.functionValues.values():
            assert i >= 0.0
        for v in self.domain.vertices:
            # Ensure that every vertex is in the domain of the function
            assert v in self.functionValues
        for l in self.domain.legs:
            # Ensure that every leg is in the domain of the function
            assert l in self.functionValues
            # Ensure that each m(l) is an integer
            assert self.functionValues[l].is_integer()
        for e in self.domain.edges:
            if e.length > 0.0:
                # Ensure the function has integer slope
                assert ((self.functionValues[e.vert1] - self.functionValues[e.vert2]) / e.length).is_integer()
    
