from ..basic_families.PiecewiseLinearFunction import *


class Family(object):
    def __init__(self, basicFamilies, morphisms):

        # Type checking
        if not isinstance(basicFamilies, set):
            raise ValueError("basicFamilies must be a Set[BasicFamily]")
        if not isinstance(morphisms, set):
            raise ValueError("morphisms must be a Set[BasicFamilyMorphism]")

        # Ensure that the morphisms actually belong in this family
        for morphism in morphisms:
            assert morphism.domain in basicFamilies
            assert morphism.codomain in basicFamilies

        self.basicFamilies = basicFamilies
        self.morphisms = morphisms

    # Returns the set of ancestors of the given basic family
    def getAncestors(self, basicFamily):

        # Type checking
        assert isinstance(basicFamily, BasicFamily)

        # Get the morphisms that map into the given basic family
        def isIncoming(morphism):
            return morphism.codomain == basicFamily
        incomingArrows = filter(isIncoming, self.morphisms)

        # Get the set of domains of the morphisms that map into the given basic family
        return {arrow.domain for arrow in incomingArrows}

    # Returns the maximal ancestors of the given basic family
    def getMaximalAncestors(self, basicFamily):

        # Type checking
        assert isinstance(basicFamily, BasicFamily)

        # Get the morphisms that map into the given basic family from a maximal family
        def isIncoming(morphism):
            return morphism.codomain == basicFamily
        incomingArrows = filter(isIncoming, self.maximalCurvesIter())

        # Get the set of domains of the morphisms that map into the given basic family
        return {arrow.domain for arrow in incomingArrows}

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

    def subdivide(self, basicFamily: BasicFamily, elt):
        """
        Subdivides the family in place at ``basicFamily`` and ``elt``

        This function subdivides the family in place. ``basicFamily`` is replaced with three other
        basic families, all of which are obtained by modifying the underlying monoid of ``basicFamily``.
        Letting ``M`` denote the monoid associated to ``basicFamily``, the three new basic families are
        identical to ``basicFamily`` except their underlying monoids are ``M[elt]``, ``M[-elt]``, and
        ``M[elt, -elt]``.

        Parameters
        ----------
        basicFamily : :class:`~Tropical2020.basic_families.BasicFamily.BasicFamily`
            the basic family at which to subdivide
        elt : ``basicFamily.monoid.Element``
            the element determining the subdivision

        Warnings
        --------
        ``elt`` must be an instance of ``basicFamily``'s :class:`~Tropical2020.basic_families.RPC.Monoid`.
        """

        assert isinstance(elt, basicFamily.monoid.Element), \
            "`elt` must be an element of `basicFamily`'s monoid."

        # Copy the basic family to be subdivided
        # todo: How do we copy monoid relations?
        famWithElt = basicFamily.getFullyShallowCopy()
        famWithNegElt = basicFamily.getFullyShallowCopy()
        famWithBoth = basicFamily.getFullyShallowCopy()

        # At this point, famWithElt, famWithNegElt, and famWithBoth are supposed to be ready.
        # todo: How do we copy monoid homomorphisms?

        pass

    def getSubdivision(self, basicFamily: BasicFamily, elt):
        """
        Returns the subdivision at ``basicFamily`` and ``elt``

        This function deeply copies the family, calls
        :func:`~Tropical2020.general_families.Family.Family.subdivide` on the copy, and then returns it.

        Parameters
        ----------
        basicFamily : :class:`~Tropical2020.basic_families.BasicFamily.BasicFamily`
            the basic family at which to subdivide
        elt : ``basicFamily.monoid.Element``
            the element determining the subdivision

        Warnings
        --------
        ``elt`` must be an instance of ``basicFamily``'s :class:`~Tropical2020.basic_families.RPC.Monoid`.
        """

        pass
