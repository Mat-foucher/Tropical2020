from ..basic_families.PiecewiseLinearFunction import *
from .Family import *


class PLFFamily(object):
    # domain: Family
    # functions: Dictionary[BasicFamily, SPLF]
    def __init__(self, domain, functions):

        # Type checking
        assert isinstance(domain, Family)
        assert isinstance(functions, dict)

        # Make sure functions actually is an assignment of functions on the family
        assert set(functions.keys()) == domain.basicFamilies, \
            "'functions' should assign something to each basic family."
        for key in functions:
            assert isinstance(functions[key], PiecewiseLinearFunction), \
                "functions[key] should be a piecewise linear function."
            assert functions[key].domain == key, \
                "functions[key] should have key as its domain."

        self.domain = domain
        self.functions = functions

        if not self.isWellDefined():
            raise ValueError("The given functions are not compatible with each other.")

    def morphismPreservesFunctions(self, morphism):

        assert morphism in self.domain.morphisms, "The given morphism should belong to the domain family."

        domainPLF = self.functions[morphism.domain]
        pushforwardPLF = domainPLF.getPushforward(morphism)
        codomainPLF = self.functions[morphism.codomain]

        return pushforwardPLF == codomainPLF

    def isWellDefined(self):
        for morphism in self.domain.morphisms:
            if not self.morphismPreservesFunctions(morphism):
                return False
        return True