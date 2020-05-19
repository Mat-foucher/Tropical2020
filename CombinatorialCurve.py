class vertex(object):
    # The vertex Class will assign each vertex their distinct properties, such as the genus.
    def __init__(self, vname_, genus_, numEdges):
        if genus_ < 0:
            raise ValueError("Genus must be nonnegative")

        self._vname = vname_
        self._genus = genus_

    @property
    def vname(self):
        return self._vname

    @vname.setter
    def vname(self, vname_):
        self._vname = vname_

    @property
    def genus(self):
        return self.genus

    @genus.setter
    def genus(self, genus_):
        if genus_ < 0:
            raise ValueError("Genus must be non-negative.")
        self._genus = genus_


class edge:
    def __init__(self, ename_, length_, vec1_, vec2_):
        if length_ < 0.0:
            raise ValueError("Length must be non-negative.")
        self._ename = ename_
        self._length = length_

        #Endpoints
        self.vec1 = vec1_
        self.vec2 = vec2_

    @property
    def ename(self):
        return self._ename

    @ename.setter
    def ename(self, ename_):
        self._ename = ename_

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
        return Set(self._vec1, self._vec2)




class CombCurve(object):

    def __init__(self, name):
        self._name = name
        self._vertices = []
        self._edges = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name_):
        self._name = name_


    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, vertices_):
        self._vertices = vertices_


    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, edges_):
        self._edges = edges_





    @property
    def vertexNumber(self):
        return len(self.vertices)

    @property
    def edgeNumber(self):
        return len(self.edges)


    def showNumbers(self):
        print "Number of Vertices: ", self.vertexNumber, " Number of Edges: ", self.edgeNumber


