# A vertex has a name and non-negative genus
class vertex(object):
    def __init__(self, name_, genus_):
        if genus_ < 0:
            raise ValueError("Genus must be non-negative")

        self.name = name_
        self._genus = genus_

    @property
    def genus(self):
        return self._genus

    @genus.setter
    def genus(self, genus_):
        if genus_ < 0:
            raise ValueError("Genus must be non-negative.")
        self._genus = genus_

# An edge has a name, non-negative length, and endpoints
class edge(object):
    def __init__(self, name_, length_, vec1_, vec2_):
        self.name = name_

        if length_ < 0.0:
            raise ValueError("Length must be non-negative.")
        self._length = length_

        #Endpoints
        self.vec1 = vec1_
        self.vec2 = vec2_

    @property
    def length(self):
        return self._length

    @length.setter
    def setLength(self, length_):
        if length_ < 0.0:
            raise ValueError("Length must be non-negative.")
        self._length = length_

    @property
    def vertices(self):
        return {self.vec1, self.vec2}

#A leg has a name and root
class leg(object):
    def __init__(self, name_, root_):
        self.name = name_
        self.root = root_

    @property
    def vertices(self):
        return {self.root}

# A Combinatorial Tropical Curve has a name, set of edges, and set of legs
class CombCurve(object):

    def __init__(self, name_):
        self.name = name_
        self._edges = {}
        self._legs = {}


    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, edges_):
        self._edges = edges_

    @property
    def legs(self):
        return self._legs

    @legs.setter
    def legs(self, legs_):
        self._legs = legs_

    @property
    def vertices(self):
        unflattened_vertex_list = [e.vertices for e in self.edges] + [l.vertices for l in self.legs]
        flattened_vertex_list = []
        for sublist in unflattened_vertex_list:
            for vertex in sublist:
                flattened_vertex_list.append(vertex)
        return set(flattened_vertex_list)

    @property
    def vertexNumber(self):
        return len(self.vertices)

    @property
    def edgeNumber(self):
        return len(self.edges)


    def showNumbers(self):
        print "Number of Vertices: ", self.vertexNumber, " Number of Edges: ", self.edgeNumber

    def showVertices(self):
        print [v.name for v in self.vertices]

    def showEdges(self):
        print [e.name for e in self.edges]

    def showLegs(self):
        print [l.name for l in self.legs]

    def degree(self, v):
        return sum(1 for e in self.edges if e.vec1 == v) + sum(1 for e in self.edges if e.vec2 == v) + sum(1 for l in self.legs if l.root == v)

    @property
    def bettiNumber(self):
        return self.edgeNumber - self.vertexNumber + 1

    @property
    def genus(self):
        return self.bettiNumber + sum([v.genus for v in self.vertices])


class StrictPiecewiseLinearFunction(object):
    def __init__(self, domain_, functionValues_):
        self._domain = domain_
        self._functionValues = functionValues_
        self.assertIsAffineLinear()

    @property
    def domain(self):
        return self._domain 

    @property
    def functionValues(self):
        return self._functionValues

    def assertIsAffineLinear(self):
        # Assert Non-Negativity at every iteration of the loop!
        
        for i in self.functionValues.values():
            assert i >= 0.0

        for v in self.domain.vertices:
            assert v in self.functionValues
        for l in self.domain.legs:
            assert l in self.functionValues
            assert self.functionValues[l].is_integer()
        for e in self.domain.edges:
            if e.length > 0.0:
                assert ((self.functionValues[e.vec1] - self.functionValues[e.vec2]) / e.length).is_integer()
    
