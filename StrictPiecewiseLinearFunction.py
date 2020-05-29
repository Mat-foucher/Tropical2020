from CombinatorialCurve import *

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
        for e in self.domain.edgesWithVertices:
            if e.length > 0.0:
                # Ensure the function has integer slope
                ((self.functionValues[e.vert1] - self.functionValues[e.vert2]) / e.length).is_integer()

    def __add__(self, other):
        assert other.domain == self.domain

        newFunctionValues = {}
        for v in self.domain.vertices:
            newFunctionValues[v] = self.functionValues[v] + other.functionValues[v]
        for leg in self.domain.legs:
            newFunctionValues[leg] = self.functionValues[leg] + other.functionValues[leg]

        return StrictPiecewiseLinearFunction(self.domain, newFunctionValues)
    
    def __sub__(self, other):
        assert other.domain == self.domain

        newFunctionValues = {}
        for v in self.domain.vertices:
            newFunctionValues[v] = self.functionValues[v] - other.functionValues[v]
        for leg in self.domain.legs:
            newFunctionValues[leg] = self.functionValues[leg] - other.functionValues[leg]

        return StrictPiecewiseLinearFunction(self.domain, newFunctionValues)

    def __mul__(self, other):
        assert other.domain == self.domain

        newFunctionValues = {}
        for v in self.domain.vertices:
            newFunctionValues[v] = self.functionValues[v] * other.functionValues[v]
        for leg in self.domain.legs:
            newFunctionValues[leg] = self.functionValues[leg] * other.functionValues[leg]

        return StrictPiecewiseLinearFunction(self.domain, newFunctionValues)

    def floodfillVertices(self, vert, S, T, allowedVertices=None):

        if allowedVertices is None:            
            allowedVertices = self.domain.vertices        
        
        edgesToCheck = {e for e in self.domain.edges if (vert in e.vertices and vert in allowedVertices)}
        print("S verts: ")
        for e in S:
            print(e.name)

        print("T verts: ")
        for f in T:
            print(f.name)

        edgesVisited = set()

        foundAnSVertex = False        
        foundATVertex = False        
        while len(edgesToCheck) > 0:
            nextEdge = edgesToCheck.pop()
            edgesVisited = edgesVisited | {nextEdge}
            # Check something here
            if (nextEdge.vert1 in T and nextEdge.vert1 in allowedVertices) or (nextEdge.vert2 in T and nextEdge.vert2 in allowedVertices):
                foundATVertex = True
            if (nextEdge.vert1 in S and nextEdge.vert1 in allowedVertices) or (nextEdge.vert2 in S and nextEdge.vert2 in allowedVertices):
                foundAnSVertex = True
            if foundATVertex and foundAnSVertex:
                return True            
        
            edgesToCheck = edgesToCheck | ({e for e in self.domain.edges if (nextEdge.vert1 in e.vertices and e.vert1 in allowedVertices and e.vert2 in allowedVertices)} - edgesVisited) 
            edgesToCheck = edgesToCheck | ({e for e in self.domain.edges if (nextEdge.vert2 in e.vertices and e.vert1 in allowedVertices and e.vert2 in allowedVertices)} - edgesVisited)

        print("S:", foundAnSVertex, "T:", foundATVertex)
        return False


    def getSpecialSupport(self):
        
        supportEdges = set()
        supportVertices = set()

        for x in self.domain.edges:
            if x.vert1 != None and x.vert2 != None:
                if self.functionValues[x.vert1] > 0 or self.functionValues[x.vert2] > 0:
                    supportEdges = supportEdges | {x}
        
        for i in self.domain.vertices:
            if self.functionValues[i] > 0:
                supportVertices = supportVertices | {i}

        return (supportEdges, supportVertices)

    
    def getSpecialSupportPartition(self):

        supportEdges, supportVertices = self.getSpecialSupport()
        connectedComponents = []
        supportVerticesNeedingComponent = list(supportVertices)
        while supportVerticesNeedingComponent != []:
            v = supportVerticesNeedingComponent[0]
            verticesToCheck = [v]
            supportComponentEdges = set()
            while verticesToCheck != []:
                currentVertex = verticesToCheck[0]
                for e in supportEdges - supportComponentEdges:
                    if currentVertex in e.vertices:
                        supportComponentEdges = supportComponentEdges | {e}
                        if e.vert1 in supportVertices:
                            verticesToCheck = verticesToCheck + [e.vert1]
                        if e.vert2 in supportVertices:
                            verticesToCheck = verticesToCheck + [e.vert2]
                
                verticesToCheck.remove(currentVertex)
                if currentVertex in supportVerticesNeedingComponent:
                    supportVerticesNeedingComponent.remove(currentVertex)
            
            connectedComponents.append(supportComponentEdges)

        return connectedComponents

    def floodfillVertices(self, vert, supportEdges, core):        
        edgesToCheck = {e for e in self.domain.edges if vert in e.vertices}
        edgesVisited = set()
        foundANonsupportVertex = False        
        foundACoreVertex = False

        while len(edgesToCheck) > 0:            
            nextEdge = edgesToCheck.pop()            
            edgesVisited = edgesVisited | {nextEdge}                        
            # Check something here            
                       
            if nextEdge.vert1 in core.vertices or nextEdge.vert2 in core.vertices:                
                foundACoreVertex = True       

            for i in supportEdges: 
                if nextEdge.vert1 not in i.vertices or nextEdge.vert2 not in i.vertices:                
                    foundANonsupportVertex = True     

            if foundACoreVertex and foundANonsupportVertex:
                return True            
                                    
            edgesToCheck = edgesToCheck | ({e for e in self.domain.edges if nextEdge.vert1 in e.vertices} - edgesVisited)
            edgesToCheck = edgesToCheck | ({e for e in self.domain.edges if nextEdge.vert2 in e.vertices} - edgesVisited)

        return False
            
        
    
    def mesaTest(self):

        # Part 1
        for i in self.domain.legs:
            if self.functionValues[i] != 0.0:
                return False 
        
        specialSupports = self.getSpecialSupportPartition()

        # Part 2
        for j in specialSupports:
            
            support = CombCurve("support")
            support.addEdges(j)

            supportCore = support.core

            assert support.isConnected
                
            if support.genus != 1:
                # support.showEdges
                print("Not Genus 1")
                return False

            const = 0.0
            previous = 0.0

            # Part 3
            # Check that the function is constant over the core of associated support:
            
            for x in supportCore.vertices:
                if const != previous:
                    print("Not Constant on core")
                    return False
                const = self.functionValues[x]
                previous = const        

            # Part 4
            allSupportVertices = {v for v in self.domain.vertices if self.functionValues[v] > 0}
            thisComponentSupportVertices = allSupportVertices.intersection(support.vertices)

            S = supportCore.vertices
            T = self.domain.vertices - allSupportVertices 

            for v in thisComponentSupportVertices: 
                
                if not self.floodfillVertices(v, S, T): 
                    print(v.name, v.genus, "Failed Part 4")
                    return False

            # Part 5 
            edgesToCheck = support.edges - supportCore.edges
            
            # Part 6 (Implemented into 5)
            atLeastOne = False

            for x in edgesToCheck:
                P = supportCore.vertices.intersection(allSupportVertices)
                vert1TowardsCore = self.floodfillVertices(x.vert1, P, P, self.domain.vertices - {x.vert2})
                if vert1TowardsCore:
                    rise = self.functionValues[x.vert1] - self.functionValues[x.vert2]
                else:
                    rise = self.functionValues[x.vert2] - self.functionValues[x.vert1]
        print("A Mesa I Am")
        return True

