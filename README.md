# Tropical2020
Classifying Tropical Surfaces Research Summer 2020 - CU Boulder

## Contents:

1. [Introduction](#Introduction)
2. [Testing](#Testing)
3. [Combinatorial Curves](#CombCurves)
4. [Strict Piecewise Linear Functions](#SPLFs)
5. [Moduli Spaces](#ModSpaces)

## Introduction <a name="Introduction"></a>

### What is the code, and how to use it:

The code for this project is divided into separate files, each for different classes that implement objects from the 
overleaf document.

The different files and their associated classes/purposes are:

- `CombinatorialCurve.py`: Vertices, Edges, Legs, and Basic Families.
- `GraphIsoHelper.py`: Provides convenience functions for testing if two graphs are isomorphic.
- `StrictPiecewiseLinearFunction.py`: Piecewise Linear functions over Basic Families.
- `ModuliSpaces.py`: Tropical Moduli spaces.
- `RPC.py`: Abstract monoids.
- `tests.py`: Tests for most things. This file is a good place to see how things are used.
- `generateAndSaveModuliSpace.py`: A short script to generate and save a moduli space as specified by command line
arguments.

## Testing <a name="Testing"></a>

The `tests.py` file is where most of the actual code is used for purposes concerning the research project. 
You may use the tests file for any test you would like to try, using the code from other files.
In `tests.py` there is also a large collection of examples from the reference document, for example, 
here is example 3.5:

    C = CombCurve("Example 3.5")
    
    M = Monoid()
    M.addgen("a")
    alpha = M.Element({"a": 1})

    v1 = vertex("v1", 0)
    v2 = vertex("v2", 0)
    v3 = vertex("v3", 1)
    e1 = edge("e1", alpha, v1, v2)
    e2 = edge("e2", alpha, v2, v3)
    e3 = edge("e3", alpha, v1, v3)
    e4 = edge("e4", alpha, v1, v1)
    l = leg("l", v1)

    C.monoid = M
    C.addEdges({e1, e2, e3, e4})
    C.addLeg(l)

Most of the tests take the form of assertions, such as:

    assert C.isConnected()
    assert C.genus == 3

## Combinatorial Curves <a name="CombCurves"></a>

1. [Vertices](#vertices)
2. [Edges](#edges)
3. [Legs](#legs)
4. [CombCurves](#combCurves)
5. [A Neat Example](#neatExample)

Vertices, Edges, Legs, Combinatorial Tropical Curves, and Basic Families of curves are implemented in 
`CombinatorialCurve.py`.

### Vertices <a name="vertices"></a>

The `vertex` class specifies the vertex object, which will always need a name (`string`) and a genus (`int` value).
In this class is a function to set the genus and a property to return the genus of the vertex.
If we want to declare a nex vertex, we can do so like in this example:

        v1 = vertex("v1", 1)

Where `"v1"` is the name of the vertex `v1`, and `v1` has a genus 1.
NOTE: The genus must always be non-negative, else an error is raised.

### Edges <a name="edges"></a>

The edges are similar to the vertices, as you may have already guessed.
For edge objects, each edge has a name in their definition, much like the vertices.
The edge object also includes a `float` parameter called length (non-negative, of course), and inputs for TWO vertices.

NOTE: For "self - edges" on the curve, you can input the same vertex for both positions.

To create an edge, one writes something like the following:

        e1 = edge("e1", 1.0, v1, v2)
    
This is an edge with name `"e1"` or edge one, and `e1` has length 1.0 and goes from vertex `v1` to vertex `v2` (assuming 
these vertices were previously defined).
Included in the class definition of edge(), there are a few functions that do what you'd pretty much expect like 
in vertices, such as getting the length (`length()`),
setting the length (`length(length_)`) and lastly returning the vertices.
Since this is python 3, we have access to the `set()` object, an unindexed list. When the function `vertices()` in 
`edge` is called, this will return a set with two elements:
the vertices that the edge connects.

### Legs <a name="legs"></a>
The leg object is much like edge, except for the fact that the leg object can only be assigned a singe vertex that it is connected to.
Unlike the other graph objects too, the leg does not have any length or genus, making it the simplest class in the file.

To create a new leg, this can be done so by the following:

    l1 = leg("l1", v1)

### CombCurves <a name="combCurves"></a>

The `CombCurve` class (short for Combinatorial Tropical Curve) provides an implementation both for combinatorial
tropical curves and basic families of tropical curves. The difference between these two interpretations is the monoid
that one provides to the class. In order to use a `CombCurve` as a combinatorial tropical curve, use a free monoid with
one generator. For example, to create a three-element chain `v1--v2--v3` with the left edge of length one and right edge
of length two, one could write the following:

    # Initialize vertices
    v1 = vertex("v1", 0)
    v2 = vertex("v2", 0)
    v3 = vertex("v3", 0)
    
    # Set up a free monoid with one generator
    M = Monoid()
    M.addgen("a")
    alpha = M.Element({"a": 1})
    
    # Edges whose lengths depend on the generator alpha
    e1 = edge("e1", alpha, v1, v2)
    e2 = edge("e2", 2 * alpha, v2, v3)
    
    # Initialize the curve
    C = CombCurve("A particular chain with three elements")
    C.addEdges({e1, e2})

One can also use `CombCurve` to represent a basic family of curves. To represent the family of three-element chains
whose edge lengths vary freely over 
<img src="https://render.githubusercontent.com/render/math?math=\mathbb{R}_{\geq 0}">, we simply use a different monoid.
Since we want two edge lengths to vary independently, we use a free monoid with two generators, and let the edge length
of each each to be one of the generators. Here is the full example:

    # Initialize vertices
    v1 = vertex("v1", 0)
    v2 = vertex("v2", 0)
    v3 = vertex("v3", 0)
    
    # Set up a free monoid with one generator
    M = Monoid()
    M.addgen("a")
    M.addgen("b")
    alpha = M.Element({"a": 1})
    beta = M.Element({"b": 1})
    
    # Edges whose lengths depend on the generator alpha
    e1 = edge("e1", alpha, v1, v2)
    e2 = edge("e2", beta, v2, v3)
    
    # Initialize the curve
    C = CombCurve("Family of all chains with three elements")
    C.addEdges({e1, e2})

The difference between a `CombCurve` representing a particular curve or a basic family of curves is largely semantic.
The first example also represents the family of all three-element chains where one edge is twice as long as the other.
    

### A Neat Example <a name="neatExample"></a>
Creating a Tropical Combinatorial Curve with the Code:

We are now ready to discuss how we may go about implementing a tropical curve in the code.
To begin, the CombCurve object is what will be the tropical curve.
As per the overleaf reference guide, the CombCurve class has the sufficent properties of behaving properly according to the definitions in the reference.

To define a new tropical curve, we write the following:

    TropicalCurve = CombCurve("TropicalCurve")

The CombCurve object takes only one parameter in it's initializer, which is the name string.
We now want to add edges, vertices, and legs to our curve, which we do deine as:

    v1 = vertex("v1", 1)
    v2 = vertex("v2", 0)
    e1 = edge("e1", v1, v2)
    l1 = leg("l1", v2)
    l2 = leg("l2", v2)

    vertices = {v1, v2}
    edges = {e1}
    legs = {l1,l2}

    TropicalCurve.addEgdes(edges)
    TropicalCurve.addLegs(legs)
    TropicalCurve.addVertices(vertices)

## Strict Piecewise Linear Functions <a name="SPLFs"></a>

## Moduli Spaces <a name="ModSpaces"></a>

1. [Basic Usage](#modSpaceUsage)
2. [Members of `TropicalModuliSpace`](#modSpaceMembers)
3. [Generating the Strata](#modSpaceStrataGen)
4. [Generating the Contraction Dictionary](#modSpaceContractionGen)
5. [Saving and Loading Spaces](#modSpaceIO)

### Basic Usage <a name="modSpaceUsage"></a>

The class `TropicalModuliSpace` found in `ModuliSpaces.py` is meant to represent the 
tropical moduli spaces <img src="https://render.githubusercontent.com/render/math?math=\mathcal{M}_{g, n}^{trop}">.
To initialize this class, an integer for the genus and marking of the moduli space must be provided. Since generating 
certain moduli spaces is very time-consuming, the generation of the space does not occur at initialization. Instead, 
a separate function call is used. For example, to generate 
<img src="https://render.githubusercontent.com/render/math?math=\mathcal{M}_{1, 5}^{trop}"> and track the time to 
generate the space, one could write the following code:

    import time
    
    m = TropicalModuliSpace(1, 5)
    
    start_time = time.time()
    m.generateSpaceDFS()
    end_time = time.time()
    
    print("Generation time:", end_time - start_time)
    
Once the moduli space has been generated, one can call `m.generateContractionDictionary()` to find what curves are
contractions of others.

If execution time is not a concern, then the full generation of 
<img src="https://render.githubusercontent.com/render/math?math=\mathcal{M}_{g, n}^{trop}"> consists of calling the
following three lines of code:

    m = TropicalModuliSpace(g, n)
    m.generateSpaceDFS()
    m.generateContractionDictionary()
    
### Members of `TropicalModuliSpace` <a name="modSpaceMembers"></a>

- `curves`: A `Set[CombCurve]` to store the strata of the space.
- `curvesDict`: A `Dictionary[Int, CombCurve]` organizing the strata by their number of edges.
- `contractionDict`: A `Dictionary[CombCurve, List[(Edge, CombCurve)]]` recording the contraction information of the
space. Given a curve `C`, `contractionDict[C]` is a list of elements of the type `(Edge, CombCurve)`. 
An element `(e, C')` belongs to `contractionDict[C]` if and only if the weighted edge contraction `C/{e}` is
isomorphic to `C'` and `C'` belongs to the space.

### Generating the Strata <a name="modSpaceStrataGen"></a>

In order to generate the strata of the moduli space, use the function `generateSpaceDFS`. This function first adds the 
unique `n`-marked stable curve of genus `g` with zero edges to the `curves` member. Then, the program examines which 
strata can be specialized, and adds these specializations to `curves` if they are novel (up to isomorphism). The 
specializations are produced in two ways: by splitting and genus-reducing vertices. These two processes are described
below and together generate all specializations.

This process is performed in a depth-first manner: As soon as a curve `C` is specialized to another curve `C'`, the
specializations of `C'` are generated.

#### Splitting Specialization

One way that curves are specialized is by splitting vertices. Given a vertex `v` of curve `C`, a nonnegative
 integer partition
`(g1, g2)` of the genus of `v`, and a partition `(S, T)` of the
endpoints of edges at `v`, a specialization of `C` can be constructed as follows. First, delete vertex `v` and 
add two vertices `v1` and `v2`. Let the genus of `v1` be `g1` and let the genus of `v2` be `g2`. Connect each
endpoint in `S` to `v1` and each endpoint in `T` to `v2`. Finally, add an edge from `v1` to `v2`.

For example, consider the following portion of a tropical curve. A single genus-3 vertex and some connecting edges are
displayed.

![Alt text](Images/pre-split.svg)

In order to partition the genus of this vertex, let `g1=2`, `g2=1`. To partition the endpoints of edges, 
let `S` contain
the connected endpoint of `e2` and the first endpoint of `e1`. Accordingly, let `T` contain the connected endpoint of
`e3`, the second endpoint of `e1`, and the root of `l`. The result is displayed below:

![Alt text](Images/post-split.svg)

The idea behind this type of specialization is to split a vertex into two pieces and distribute its data among those
pieces.

In order to preserve stability, there are some restrictions on `g1`, `g2`, `S`, and `T`. If `g1=0`, then `S` must
contain at least two elements. Otherwise, after splitting, a vertex of genus zero would have degree less than three.
Similarly, if `g2=0`, then `T` must have at least two elements.

#### Genus Reduction Specialization

Another way that curves are specialized is by reducing the genus of vertices. Given a vertex `v` of a curve `C`, a
specialization of `C` can be produced in the following manner as long as `v` has genus at least one. To produce the
specialization of `C`, simply reduce the genus of `v` and introduce a new edge connecting `v` to itself. Taking the 
same example as was used for the splitting specialization, consider the following portion of a curve:

![Alt text](Images/pre-split.svg)

This vertex has positive genus, so we can reduce the genus and introduce a new loop:

![Alt text](Images/post-genus-reduction.svg)

As with splitting specialization, this type of specialization does not necessarily preserve stability. The one case 
where stability is not preserved is when `v` is a vertex with genus one and degree zero. If this vertex were
genus-reduced, it would become a vertex with genus zero and degree two.

### Generating the Contraction Information <a name="modSpaceContractionGen"></a>

In order to generate the contraction dictionary of the moduli space, use the function `generateContractionDictionary`.
For each curve `C` in the space, and for each edge `e` of `C`, this function identifies which curve of the space is
isomorphic to the weighted edge contraction `C/{e}`.

### Saving and Loading Spaces <a name="modSpaceIO"></a>

In order to load a moduli space from a file, initialize the space with proper genus and marking number, and then call 
`loadModuliSpaceFromFile(filename)`. To save a space, call `saveModuliSpaceToFile`. Both functions accept delimiter
and encoding information. By default, the curve entry delimiter is `=` and the encoding is `utf-8`. 
`saveModuliSpaceToFile` accepts an optional filename to save to. If none is provided, a filename is automatically
generated based on the genus and marking of the space.
