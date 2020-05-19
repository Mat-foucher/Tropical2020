class vertex(object):
    # The vertex Class will assign each vertex their distinct properties, such as the genus.
    def __init__(self, name_, genus_, numEdges):
        if genus_ < 0:
            raise ValueError("Genus must be nonnegative")

        self.name = name_
        self._genus = genus_

    @property
    def genus(self):
        return self.genus

    @genus.setter
    def genus(self, genus_):
        if genus_ < 0:
            raise ValueError("Genus must be non-negative.")
        self._genus = genus_


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




class CombCurve(object):

    def __init__(self, name):
        self.name = name
        self._edges = {}


    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, edges_):
        self._edges = edges_

    @property
    def vertices(self):
        unflattened_vertex_list = [e.vertices for e in self.edges]
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

