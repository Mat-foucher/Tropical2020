from CombinatorialCurve import *
from ModuliSpaces import *


class PiecewiseLinearFunction(object):
    # domain_ should be a CombCurve representing the domain of the function
    # functionValues_ should be a dictionary with vertex/leg keys and non-negative double values
    def __init__(self, domain_, functionValues_):
        self._domain = domain_
        self._functionValues = functionValues_
        self.assertIsWellDefined()
        self.generateVertexValues()
        # self.assertIsAffineLinear()

    # Make the domain read only
    @property
    def domain(self):
        return self._domain

        # Make the function read only

    @property
    def functionValues(self):
        return self._functionValues

    def propogateVertexValues(self, tree):
        for child, connectingEdge in tree.children:

            if connectingEdge.vert1 == tree.value:
                orientation = 1
            else:
                orientation = -1

            self.functionValues[child.value] = self.functionValues[tree.value] + \
                                               (orientation * self.functionValues[connectingEdge]) * connectingEdge.length
            self.propogateVertexValues(child)

    # Todo - Figure out how to handle a disconnected domain
    def generateVertexValues(self):
        if len(self.domain.vertices) <= 0:
            return

        # Get any domain vertex

        if len(self.domain.vertices.intersection(self._functionValues.keys())) > 0:
            baseVert = self.domain.vertices.intersection(self._functionValues.keys()).pop()
            tree = self.domain.getSpanningTree(baseVert)
            self.propogateVertexValues(tree)
        else:
            baseVert = list(self.domain.vertices)[0]
            tree = self.domain.getSpanningTree(baseVert)
            self.functionValues[tree.value] = self.domain.monoid.zero()
            self.propogateVertexValues(tree)

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
        for e in self.domain.edgesWithVertices:
            if e.length > 0.0:
                # Ensure the function has integer slope
                ((self.functionValues[e.vert1] - self.functionValues[e.vert2]) / e.length).is_integer()

    def __add__(self, other):
        assert other.domain == self.domain

        newFunctionValues = {}
        for e in self.domain.edges:
            newFunctionValues[e] = self.functionValues[e] + other.functionValues[e]
        for leg in self.domain.legs:
            newFunctionValues[leg] = self.functionValues[leg] + other.functionValues[leg]

        return PiecewiseLinearFunction(self.domain, newFunctionValues)

    def __sub__(self, other):
        assert other.domain == self.domain

        newFunctionValues = {}
        for e in self.domain.edges:
            newFunctionValues[e] = self.functionValues[e] - other.functionValues[e]
        for leg in self.domain.legs:
            newFunctionValues[leg] = self.functionValues[leg] - other.functionValues[leg]

        return PiecewiseLinearFunction(self.domain, newFunctionValues)

    def __eq__(self, other):
        if not isinstance(other, PiecewiseLinearFunction):
            print("Wrong types")
            return False

        if not self.domain != other.domain:
            print("Different domains")
            return False

        for nextVertex in self.domain.vertices:
            if self.functionValues[nextVertex] != other.functionValues[nextVertex]:
                print("Different function values!")
                return False

        return True

    def printSelf(self):
        for v in self.domain.vertices:
            print(v.name, self.functionValues[v].coeffs)
        for e in self.domain.edges:
            print(e.name, self.functionValues[e])
        
        for l in self.domain.legs:
            print(l.name, self.functionValues[l])

    def floodfillVertices(self, vert, S, T, allowedVertices=None):

        if allowedVertices is None:
            allowedVertices = self.domain.vertices

        edgesToCheck = {e for e in self.domain.edges if (vert in e.vertices and vert in allowedVertices)}

        edgesVisited = set()

        foundAnSVertex = False
        foundATVertex = False
        while len(edgesToCheck) > 0:
            nextEdge = edgesToCheck.pop()
            edgesVisited = edgesVisited | {nextEdge}
            # Check something here
            if (nextEdge.vert1 in T and nextEdge.vert1 in allowedVertices) or (
                    nextEdge.vert2 in T and nextEdge.vert2 in allowedVertices):
                foundATVertex = True
            if (nextEdge.vert1 in S and nextEdge.vert1 in allowedVertices) or (
                    nextEdge.vert2 in S and nextEdge.vert2 in allowedVertices):
                foundAnSVertex = True
            if foundATVertex and foundAnSVertex:
                return True

            edgesToCheck = edgesToCheck | ({e for e in self.domain.edges if (
                    nextEdge.vert1 in e.vertices and e.vert1 in allowedVertices and e.vert2 in allowedVertices)} - edgesVisited)
            edgesToCheck = edgesToCheck | ({e for e in self.domain.edges if (
                    nextEdge.vert2 in e.vertices and e.vert1 in allowedVertices and e.vert2 in allowedVertices)} - edgesVisited)

        # print("S:", foundAnSVertex, "T:", foundATVertex)
        return False

    # Returns twice the integral of self over the supplied path
    def doubleIntegrateOverLoop(self, loop):
        if len(loop) == 0:
            return self.domain.monoid.zero()
        if len(loop) == 1:
            if loop[0].vert1 != loop[0].vert2:
                raise ValueError("The supplied list of edges is not a loop.")
            return self.functionValues[loop[0]] * loop[0].length

        # Loops of length 2 are weird...
        if len(loop) == 2:
            if loop[0].vertices != loop[1].vertices:
                raise ValueError("The supplied list of edges is not a loop.")
            # Orientation is regular
            if loop[0].vert2 == loop[1].vert1:
                return self.functionValues[loop[0]] * loop[0].length + self.functionValues[loop[1]] * loop[1].length
            else:
                return self.functionValues[loop[0]] * loop[0].length - self.functionValues[loop[1]] * loop[1].length

        integral = self.domain.monoid.zero()

        # Integrate over everything except for the very last edge of the path
        for edgeIndex in range(len(loop) - 1):
            currentEdge = loop[edgeIndex]
            nextEdge = loop[edgeIndex + 1]

            if len(currentEdge.vertices.intersection(nextEdge.vertices)) == 0:
                raise ValueError("The supplied list of edges is not a path.")
            connectingVertex = currentEdge.vertices.intersection(nextEdge.vertices).pop()

            # Passing over currentEdge from vert1 to vert 2 <=> normal orientation
            if connectingVertex == currentEdge.vert2:
                integral += self.functionValues[currentEdge] * currentEdge.length
            else:
                integral += (-1 * self.functionValues[currentEdge]) * currentEdge.length

        # Integrate over the very last edge
        secondToLastEdge = loop[len(loop) - 2]
        lastEdge = loop[len(loop) - 1]
        if len(secondToLastEdge.vertices.intersection(lastEdge.vertices)) == 0:
            raise ValueError("The supplied list of edges is not a path.")
        connectingVertex = secondToLastEdge.vertices.intersection(lastEdge.vertices).pop()

        # Passing over lastEdge from vert1 to vert 2 <=> normal orientation
        if connectingVertex == lastEdge.vert1:
            integral += self.functionValues[lastEdge] * lastEdge.length
        else:
            integral += (-1 * self.functionValues[lastEdge]) * lastEdge.length

        return integral

    def assertIsWellDefined(self):
        for l in self.domain.loops:
            assert self.doubleIntegrateOverLoop(l) == self.domain.monoid.zero()

    # We probably will not need this.
    def getEdgeSlopesFrom(self, v1, v2):

        edgesAndSlopes = {'edge': 'slope'}

        firstVertexSet = self.domain.vertices - v2
        secondVertexSet = self.domain.vertices - v1

        if not self.domain.isConnected:
            raise ValueError("Curve is disconnected, please compute edge slopes for connected components only.")

        edgesToCheckForSlope = {e for e in self.domain.edges if e.vert1 == v1}
        edgesChecked = set()

        while len(edgesToCheckForSlope) > 0:
            nextEdgeToCheck = edgesToCheckForSlope.pop()
            edgesChecked = edgesChecked | {nextEdgeToCheck}

            v1Val = 0.0

            for key, value in self.functionValues:
                if nextEdgeToCheck.vert1 == key:
                    v1Val = value

            for key, value in self.functionValues:
                if nextEdgeToCheck.vert2 == key:
                    edgesAndSlopes[key] = value - v1Val

            if (nextEdge.vert2 == v2):
                return edgesAndSlopes

            edgesToCheckForSlope = edgesToCheckForSlope | (
                    {e for e in self.domain.edges if nextEdge.vert2 in e.vertices} - edgesChecked)

        raise ValueError("No path from v1 to v2 exists")

    def getSpecialSupport(self):

        supportEdges = set()
        supportVertices = set()

        for x in self.domain.edges:
            if x.vert1 != None and x.vert2 != None:
                if self.functionValues[x.vert1] != self.domain.monoid.zero() or self.functionValues[x.vert2] != self.domain.monoid.zero():
                    supportEdges = supportEdges | {x}

        for i in self.domain.vertices:
            if self.functionValues[i] != self.domain.monoid.zero():
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

    @property
    def mesaTest(self):

        # A mesa must have slope and value zero on all legs
        for i in self.domain.legs:
            # Check that the slope is zero:
            if self.functionValues[i] != 0.0:
                return False
            # Check that the value is zero:
            if self.functionValues[i.root] != self.domain.monoid.zero():
                return False

        # specialSupports contains a list of sets. Each set in the list contains the edges of one of the connected
        # components of the support. These edges may contain vertices out of the support.
        specialSupports = self.getSpecialSupportPartition()

        # The rest of the checks must hold for each connected component of the support.
        for j in specialSupports:

            # Support component realized as a Combinatorial Curve
            support = BasicFamily("support")
            support.addEdges(j)

            # Core of the support realized as a Combinatorial Curve
            supportCore = support.core

            assert support.isConnected

            # Each component of the support must have genus 1
            if support.genus != 1:
                # support.showEdges
                print("Not Genus 1")
                return False

            # Check that the function is constant over the core of associated support:

            # Get a random function value from the support-core vertices
            coreFuncVal = self.functionValues[list(supportCore.vertices)[0]]

            # Make sure every vertex of the support core has this same value
            for vert in supportCore.vertices:
                if self.functionValues[vert] != coreFuncVal:
                    return False

            # Every vertex of the support must lie on a path from the core of the support component to a vertex outside
            # of the support
            allSupportVertices = {v for v in self.domain.vertices if self.functionValues[v] != self.domain.monoid.zero()}
            thisComponentSupportVertices = allSupportVertices.intersection(support.vertices)

            S = supportCore.vertices
            T = self.domain.vertices - allSupportVertices

            for v in thisComponentSupportVertices:

                if not self.floodfillVertices(v, S, T):
                    print(v.name, v.genus, "Failed Part 4")
                    return False

            # Check that the function has slope 0 or 1 on every edge out of the core (oriented towards the core)
            edgesToCheck = support.edges - supportCore.edges

            for nextEdge in edgesToCheck:
                # Search for the vertices of the core that actually belong to the support
                P = supportCore.vertices.intersection(allSupportVertices)

                # Check if a vertex from P can be reached from vert1 of nextEdge if we do not allow ourselves to
                # travel over vert2 of nextEdge. If this can be done, then vert1 is the side of nextEdge that is
                # closest to the core. Otherwise, it's vert2.
                vert1TowardsCore = self.floodfillVertices(nextEdge.vert1, P, P, self.domain.vertices - {nextEdge.vert2})

                # Calculate the rise of the function with respect to orientation towards the core.
                if vert1TowardsCore:
                    rise = self.functionValues[nextEdge.vert1] - self.functionValues[nextEdge.vert2]
                else:
                    rise = self.functionValues[nextEdge.vert2] - self.functionValues[nextEdge.vert1]

                # The rise is 0.0 or nextEdge.length iff the slope of the function is 0 or 1 towards the cure.
                # Both of these must hold
                if not (rise == self.domain.monoid.zero() or rise == nextEdge.length):
                    return False

            # Next, search for an edge adjacent to the core that has nonzero slope.
            specialEdgeFound = False
            for nextEdge in support.edges:
                # nextEdge is adjacent to the core if it has one endpoint in, and one endpoint out of, the core.
                adjacentToCore = (((nextEdge.vert1 in supportCore.vertices) and
                                   (nextEdge.vert2 not in supportCore.vertices)) or
                                  ((nextEdge.vert2 in supportCore.vertices) and
                                   (nextEdge.vert1 not in supportCore.vertices)))

                if adjacentToCore and self.functionValues[nextEdge.vert1] != self.functionValues[nextEdge.vert2]:
                    specialEdgeFound = True
                    break

            if not specialEdgeFound:
                return False

        # print("A Mesa I Am")
        return True

    # Computes the pushforward of self along the given morphism
    def getPushforward(self, morphism):
        assert isinstance(morphism, BasicFamilyMorphism), "morphism should be a morphism of basic families."
        assert morphism.domain == self.domain, "morphism and self should have the same domain."

        # The domain of the pushforward is the image of the morphism
        pushforwardDomain = morphism.image()

        pushforwardFunctionValues = {}
        for nextEdge in self.domain.edges:
            # If the edge does not collapse, then keep its slope.
            if morphism(nextEdge) in morphism.codomain.edges:
                pushforwardFunctionValues[morphism(nextEdge)] = self.functionValues[nextEdge]
        for nextVert in self.domain.vertices:
            pushforwardFunctionValues[morphism(nextVert)] = morphism(self.functionValues[nextVert])
        for nextLeg in self.domain.legs:
            pushforwardFunctionValues[morphism(nextLeg)] = self.functionValues[nextLeg]

        return PiecewiseLinearFunction(pushforwardDomain, pushforwardFunctionValues)

    # functionContractions will return a dictionary of curves as keys with SPLFs as values.
    def functionContractions(self):

        dictOfContractedFunctions = {}

        for e in self.domain.edges:
            contraction, copyInfo = self.domain.getContraction(e, True)

            newFunctionValues = {}

            for i in self.domain.edges:
                if copyInfo[i] in contraction.edges:
                    newFunctionValues[copyInfo[i]] = self.functionValues[i] 
            
            for l in self.domain.legs:
                newFunctionValues[copyInfo[l]] = self.functionValues[l]

            try:

                #for f in newFunctionValues:
                #    print(f.name, newFunctionValues[f])

                #contraction.printSelf()
                function = PiecewiseLinearFunction(contraction, newFunctionValues)
                function.assertIsWellDefined()
                dictOfContractedFunctions[e] = function
            except:
                #print("ERROR: In initializing function for " + contraction.name)
                pass

        return dictOfContractedFunctions