
class Family(object):
    def __init__(self):
        self.morphisms = set()


class BasicFamilyMorphism(object):
    pass


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

