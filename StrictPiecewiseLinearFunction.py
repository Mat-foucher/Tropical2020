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
        for e in self.domain.edges:
            if e.length > 0.0:
                # Ensure the function has integer slope
                assert ((self.functionValues[e.vert1] - self.functionValues[e.vert2]) / e.length).is_integer()

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