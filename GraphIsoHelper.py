from CombinatorialCurve import *


class GraphIsoHelper(object):

    @staticmethod
    def getPermutations(lst):
        # If lst is empty then there are no permutations
        if len(lst) == 0:
            return []

        # If there is only one element in lst then, only one permutation is possible
        if len(lst) == 1:
            return [lst]

        # Find the permutations for lst if there are more than 1 characters

        perms = []  # empty list that will store current permutation

        # Iterate the input(lst) and calculate the permutation
        for i in range(len(lst)):
            m = lst[i]

            # Extract lst[i] or m from the list.  remLst is
            # remaining list
            remLst = lst[:i] + lst[i + 1:]

            # Generating all permutations where m is first
            # element
            for p in GraphIsoHelper.getPermutations(remLst):
                perms.append([m] + p)
        return perms

    @staticmethod
    def getBijections(permDict):

        if len(permDict) == 0:
            return [{}]

        nextKey = list(permDict.keys())[0]
        permsOfThatKey = permDict.pop(nextKey)
        remaining = GraphIsoHelper.getBijections(permDict)

        perms = []

        for perm in permsOfThatKey:
            for subPerm in remaining:
                # Taking the union of dictionaries in python is next to impossible to do nicely :(
                newDict = {nextKey: perm}
                for k in subPerm:
                    newDict[k] = subPerm[k]
                perms.append(newDict)
        return perms

    @staticmethod
    def checkIfBijectionIsIsomorphism(domain, codomain, domainOrderingDict, codomainOrderingDict):

        keyList = list(domainOrderingDict.keys())

        inputList = []
        outputList = []
        for key in keyList:
            inputList = inputList + domainOrderingDict[key]
            outputList = outputList + codomainOrderingDict[key]

        # print("Checking input list: ", [v.name for v in inputList])
        # print("With corresponding output list: ", [v.name for v in outputList])

        for i in range(len(inputList)):
            for j in range(len(inputList)):
                # Number of edges connecting inputList[i] and inputList[j]
                numInputEdges = sum(1 for e in domain.edges if e.vertices == {inputList[i], inputList[j]})
                numOutputEdges = sum(1 for e in codomain.edges if e.vertices == {outputList[i], outputList[j]})
                if numInputEdges != numOutputEdges:
                    # print("Function does not preserve number of connecting edges")
                    return False

        for i in range(len(inputList)):
            if inputList[i].genus != outputList[i].genus:
                # print("Function does not preserve genus")
                return False
            numInputLegs = sum(1 for nextLeg in domain.legs if nextLeg.root == inputList[i])
            numOutputLegs = sum(1 for nextLeg in codomain.legs if nextLeg.root == outputList[i])
            if numInputLegs != numOutputLegs:
                # print("Function does not preserve number of legs")
                return False

        # print("This was an isomorphism!")
        return True

    @staticmethod
    def isBruteForceIsomorphicTo(domain, codomain):
        selfEverythingVertexDict = domain.getVerticesByCharacteristic()
        otherEverythingVertexDict = codomain.getVerticesByCharacteristic()

        permDict = {}
        for d in selfEverythingVertexDict:
            permDict[d] = domain.getPermutations(selfEverythingVertexDict[d])
        domainOrderingDicts = domain.getBijections(permDict)

        for domainOrderingDict in domainOrderingDicts:
            if domain.checkIfBijectionIsIsomorphism(codomain, domainOrderingDict, otherEverythingVertexDict):
                return True

        return False

    @staticmethod
    def isIsomorphicTo(domain, codomain):
        if domain.numEdges != codomain.numEdges:
            # print("Different Number of Edges")
            return False

        if domain.numVertices != codomain.numVertices:
            # print("Different Number of Vertices")
            return False

        if domain.vertexCharacteristicCounts != codomain.vertexCharacteristicCounts:
            # print("Different counts of vertices with a given number of legs, edges, and genus")
            # print(self.getVerticesByEverything())
            # print(other.getVerticesByEverything())
            # print(self.vertexEverythingDict)
            # print(other.vertexEverythingDict)
            return False

        loop1 = domain.vertexSelfLoopDict
        loop2 = codomain.vertexSelfLoopDict
        if loop1 != loop2:
            # print("Different Instances of Self Loops")
            return False

        # print("Easy tests were inconclusive - switching to brute force")
        return domain.isBruteForceIsomorphicTo(codomain)
