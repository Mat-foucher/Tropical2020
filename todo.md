# To do

This to-do list serves to remind us of some things that would be nice to change.

## Long term tasks
1. Review / clean up existing code
2. Write documentation
3. Write tests for...
    - Morphisms of basic families

## Morphisms

1. A lot of *unstructured* code for finding isomorphisms of pure graphs exists already. Clean it up so that we actually 
have a class representing a graph homomorphism. Then, refactor the isomorphism code to revolve around this.
2. Write code for generating the following morphisms of basic families:
    1. Weighted edge contractions
    2. Automorphisms
    3. The morphism of basic families corresponding to a morphism of pure graphs
3. Write code for morphisms of marked families
    1. From an unmarked family, generate the corresponding marked families.
4. Get the image of a monoid homomorphism
5. Reversing-an-edge morphism?

## General Families

1. Make `TropicalModuliSpace` inherit from `Family`.
2. Consider moving a *lot* (i.e., almost all) of generation code from `TropicalModuliSpace` to `Family`.
    1. Most of the `TropicalModuliSpace` code is applicable to a general family.
    2. The only code that really needs to stay is the generation of `M-g-n` from the unique curve consisting of one
    genus `g` vertex rooting `n` legs.
3. Generate a family from an assignment of maximal strata (Contraction generation)
4. Generate a family from an assignment of minimal strata (Specialization generation)
5. Generate a family from any strata (previous two points)
6. Find a good basis of morphisms to consider when checking if a PLF over a family is well-defined.
    1. Currently, all morphisms of the family are checked. Conjecture: Only a transitive basis is needed.

## Graphics

1. Increase space between levels
2. Make things interactive?
3. Write code for showing a general family
