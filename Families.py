
from CombinatorialCurve import *


class Family(object):
    def __init__(self, basicFamilies, morphisms):

        # Type checking
        if not isinstance(basicFamilies, set):
            raise ValueError("basicFamilies must be a Set[CombCurve]")
        if not isinstance(morphisms, set):
            raise ValueError("morphisms must be a Set[BasicFamilyMorphism]")

        # Ensure that the morphisms actually belong in this family
        for morphism in self.morphisms:
            assert morphism.domain in self.basicFamilies
            assert morphism.codomain in self.basicFamilies

        self.basicFamilies = basicFamilies
        self.morphisms = morphisms

    # Returns an iterator of all basic families that are not contractions of any other family
    def maximalCurvesIter(self):

        def isMaximal(basicFam):

            # A basic family is not maximal if it's the codomain of some proper morphism
            for morphism in self.morphisms:
                if morphism.codomain == basicFam and morphism.domain != basicFam:
                    return False

            # If this code is reached, then no proper morphism maps into basicFam, and so it's maximal.
            return True

        return filter(isMaximal, self.basicFamilies)


class BasicFamilyMorphism(object):
    def __init__(self, domain, codomain):

        # Type checking
        if not isinstance(domain, CombCurve):
            raise ValueError("The domain of a basic family morphism must be a CombCurve.")
        if not isinstance(codomain, CombCurve):
            raise ValueError("The codomain of a basic family morphism must be a CombCurve.")

        self.domain = domain
        self.codomain = codomain



class TropicalFamily(Family):
    pass


class PLFFamily(object):
    # domain: Family
    # functions: Dictionary[BasicFamily, SPLF]
    def __init__(self, domain, functions):
        assert isinstance(domain, Family)
        assert isinstance(functions, dict)
        for key in functions:
            assert functions[key].domain == key

        self.domain = domain
        self.functions = functions

        if not self.isWellDefined():
            raise ValueError("The given functions are not compatible with each other.")

    def morphismPreservesFunctions(self, morphism):
        pass

    def isWellDefined(self):
        for morphism in self.domain.morphisms:
            if not self.morphismPreservesFunctions(morphism):
                return False
        return True

