from typing import Any, Dict, Iterator, Set, Tuple

from ..basic_families.BasicFamily import BasicFamily
from ..basic_families.BasicFamily import BasicFamilyMorphism
from ..basic_families.RPC import MonoidHomomorphism


class Family(object):
    def __init__(self, basicFamilies: Set[BasicFamily], morphisms: Set[BasicFamilyMorphism]) -> None:

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
    def getAncestors(self, basicFamily: BasicFamily) -> Set[BasicFamily]:

        # Type checking
        assert isinstance(basicFamily, BasicFamily)

        # Get the morphisms that map into the given basic family
        def isIncoming(morphism: BasicFamilyMorphism) -> bool:
            return morphism.codomain == basicFamily
        incomingArrows = filter(isIncoming, self.morphisms)

        # Get the set of domains of the morphisms that map into the given basic family
        return {arrow.domain for arrow in incomingArrows}

    # Returns the maximal ancestors of the given basic family
    def getMaximalAncestors(self, basicFamily: BasicFamily) -> Set[BasicFamily]:

        # Type checking
        assert isinstance(basicFamily, BasicFamily)

        # Get the morphisms that map into the given basic family from a maximal family
        def isIncoming(morphism: BasicFamilyMorphism) -> bool:
            return morphism.codomain == basicFamily
        incomingArrowDomains: Set[BasicFamily] = {arrow.domain for arrow in filter(isIncoming, self.morphisms)}

        maximalCurves = list(self.maximalCurvesIter())

        return {fam for fam in incomingArrowDomains if fam in maximalCurves}

    # Returns an iterator of all basic families that are not contractions of any other family
    def maximalCurvesIter(self) -> Iterator[BasicFamily]:

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

        def _invertDict(d: dict) -> dict:
            inverted = {}
            for k in d:
                inverted[d[k]] = k
            return inverted

        # returns g \circ f
        def _composeDicts(g: Dict[Any, Any], f: Dict[Any, Any]) -> Dict[Any, Any]:
            newDict = {}
            for key in f:
                newDict[key] = g[f[key]]
            return newDict

        # Copies fam, adds everything in x to its monoid, and copies appropriate arrows
        def _addElement(fam: BasicFamily, x: list) -> Tuple[BasicFamily, dict]:
            famCopy, copyInfo = fam.getFullyShallowCopy(returnCopyInfo=True)
            famCopy.monoid = famCopy.monoid.extend(gens=x)

            for arrow in self.morphisms:
                if arrow.domain == fam:
                    newMorphismDict = {}
                    invertedCopyInfo = _invertDict(copyInfo)

                    # Compose the inverse of the copying map with the arrow
                    for vertex in famCopy.vertices:
                        newMorphismDict[vertex] = arrow(invertedCopyInfo[vertex])
                    for edge in famCopy.edges:
                        newMorphismDict[edge] = arrow(invertedCopyInfo[edge])
                    for leg in famCopy.legs:
                        newMorphismDict[leg] = arrow(invertedCopyInfo[leg])

                    newMonoidMorphismMatrix = arrow.monoidMorphism.matrix
                    for gen in x:
                        newMonoidMorphismMatrix[gen] = arrow(gen)

                    arrowCopy = BasicFamilyMorphism(famCopy, arrow.codomain, newMorphismDict, newMonoidMorphismMatrix)

                    self.morphisms.add(arrowCopy)

                elif arrow.codomain == fam:
                    newMorphismDict = {}

                    # Compose arrow with the copying map
                    for vertex in arrow.domain.vertices:
                        newMorphismDict[vertex] = copyInfo[arrow(vertex)]
                    for edge in arrow.domain.edges:
                        newMorphismDict[edge] = copyInfo[arrow(edge)]
                    for leg in arrow.domain.legs:
                        newMorphismDict[leg] = copyInfo[arrow(leg)]

                    # In this case, we just need to extend the codomain
                    newMonoidMorphism = MonoidHomomorphism(arrow.domain.monoid, fam.monoid, arrow.monoidMorphism.matrix)

                    arrowCopy = BasicFamilyMorphism(arrow.domain, famCopy, newMorphismDict, newMonoidMorphism)

                    self.morphisms.add(arrowCopy)

            self.basicFamilies.add(famCopy)
            return famCopy, copyInfo

        famWithElt, copyInfoE = _addElement(basicFamily, [elt])
        famWithNegElt, copyInfoNE = _addElement(basicFamily, [-elt])
        famWithBoth, copyInfoB = _addElement(basicFamily, [elt, -elt])

        self.basicFamilies.remove(basicFamily)

        # Determines how elements of famWithElt correspond to famWithBoth
        arrowEltToBoth: BasicFamilyMorphism = BasicFamilyMorphism(
            famWithElt,
            famWithBoth,
            _composeDicts(copyInfoB, _invertDict(copyInfoE)),
            MonoidHomomorphism(famWithElt.monoid, famWithBoth.monoid)
        )
        self.morphisms.add(arrowEltToBoth)

        # Determines how elements of famWithNegElt correspond to famWithBoth
        arrowNegEltToBoth: BasicFamilyMorphism = BasicFamilyMorphism(
            famWithNegElt,
            famWithBoth,
            _composeDicts(copyInfoB, _invertDict(copyInfoNE)),
            MonoidHomomorphism(famWithNegElt.monoid, famWithBoth.monoid)
        )
        self.morphisms.add(arrowNegEltToBoth)
