
class vertex:
    # The vertex Class will assign each vertex their distinct properties, such as the genus.
    def __init__(self, vname, genus, numEdges):
        self.vname = vname
        self.genus = genus
    
    def setName(self, name_):
        self.vname = name_

    def setGenus(self, genus_):
        self.genus = genus_
    
    def getName(self):
        return self.vname
    
    def getGenus(self):
        return self.genus



# The EDGES of the combinatorial tropical curve will only have a name and length (for now).
class edge:
    def __init__(self, ename, length):
        self.ename = ename
        self.length = length

    def setName(self, name_):
        self.ename = name_

    def setLength(self, length_):
        self.length = length_

    def getName(self):
        return self.ename
    
    def getLength(self):
        return self.length


class CombCurve(vertex, edge):
   
    def __init__(self, name, vertexNumber, edgeNumber):
        self.name = name
        self.vertexNumber = vertexNumber
        self.edgeNumber = edgeNumber
        self.vertices = []
        self.edges = []

    def setName(self, name_):
        self.name = name_        
    
    def setVertexNumber(self, number_):
        self.vertexNumber = number_
    
    def setEdgeNumber(self, number_1):
        self.edgeNumber = number_1

    def getName(self):
        return self.name

    def getVertexNumber(self):
        return self.vertexNumber
    
    def getEdgeNumber(self)
        return self.edgeNumber

    def showNumbers(self):
        print "Number of Vertices: ", self.vertexNumber, " Number of Edges: ", self.edgeNumber





Curve1 = CombCurve("Curve1", 3 , 3)

Curve1.showNumbers()

