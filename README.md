# Tropical2020
Classifying Tropical Surfaces Research Summer 2020 - CU Boulder

## Contents:

1. [Introduction](#Introduction)
2. [Testing](#Testing)
3. [Combinatorial Curves](#CombCurves)
4. [Strict Piecewise Linear Functions](#SPLFs)
5. [Moduli Spaces](#ModSpaces)
6. [General Families](#Families)

## Introduction <a name="Introduction"></a>

### What is the code, and how to use it:

The code for this project is divided into separate files, each for different classes that implement objects from the 
overleaf document.

The different files are:

- StrictPiecewiseLinearFunction.py
- CombinatorialCurve.py
- ModuliSpaces.py
- RPC.py
- tests.py

## Testing <a name="Testing"></a>

The test document is where most of the actual code is used for purposes concerning the research project. 
You may use the tests document for any test you would like to try, using the code from other documents.
In the tests file there is also a large collection of examples from the overleaf document, for example, 
here is example 3.5:

            C = CombCurve("Example 3.5")

            v1 = vertex("v1", 0)
            v2 = vertex("v2", 0)
            v3 = vertex("v3", 1)
            e1 = edge("e1", 1.0, v1, v2)
            e2 = edge("e2", 1.0, v2, v3)
            e3 = edge("e3", 1.0, v1, v3)
            e4 = edge("e4", 1.0, v1, v1)
            l = leg("l", v1)

            C.addEdges({e1, e2, e3, e4})
            C.addLeg(l)

The test doc is also a fabulous place to use assertions, such as:

            assert C.isAffineLinear()

In conclusion, for those picking up this code to use for pioneering things on tropical geometry, 
most of the work will be done in tests.py

## Combinatorial Curves <a name="CombCurves"></a>

1. [Vertices](#vertices)
2. [Edges](#edges)
3. [A Neat Example](#neatExample)

The document `CombinatorialCurve.py` is for all specifications regarding the combinatorial tropical curves as seen in 
the overleaf document.
In the timeline of this project, the classes in this doc have been modified over and over and over and over again 
(lowkey kind of painful).

In this current version, the first two classes you will see in this document are the `vertex`, `edge`, and `leg` 
classes.

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

Leg:
The leg object is much like edge, except for the fact that the leg object can only be assigned a singe vertex that it is
connected to.
Unlike the other graph objects too, the leg does not have any length or genus, making it the simplest class in the file.

To create a new leg, this can be done so by the following:

    l1 = leg("l1", v1)
        

### A Neat Example <a name="neatExample"></a>
Creating a Tropical Combinatorial Curve with the Code:

We are now ready to discuss how we may go about implementing a tropical curve in the code.
To begin, the CombCurve object is what will be the tropical curve.

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

1. [Creating a Function](#splfUsage)
2. [Testing the Well - Definedness of Your SPLF](#splfDefined)
3. [Checking if Your Function is a Mesa](#splfMesa)

### Creating a Function <a name="splfUsage"></a>

The class of strict piecewise linear functions (SPLF for short) serves as the main method of searching for mesas on 
the combinatorial tropical curves as previously introduced.

The way that the class is implemented is by using a dictionary object, in which the values of the dictionary are the 
slopes of the edges of the curve, and the keys are the edges of the curve.

NOTE: There must be a defined tropical curve (`CombCurve()`) before an SPLF over the tropical curve is made.

To make an SPLF over a tropical curve, we may specify the curve as such:

```
C = CombCurve("Example 3.5")

v1 = vertex("v1", 0)
v2 = vertex("v2", 0)
v3 = vertex("v3", 1)

e1 = edge("e1", freeElementA, v1, v2)
e2 = edge("e2", freeElementA, v2, v3)
e3 = edge("e3", freeElementA, v1, v3)
e4 = edge("e4", freeElementA, v1, v1)
l = leg("l", v1)

C.addEdges({e1, e2, e3, e4})
C.addLeg(l)

#Here will be the SPLF:

dict = {e1: 1, e2: 0, e3: 1, e4: 0}

f = StrictPiecewiseLinearFunction(C, dict)

```

As can be seen in the block of code, the `StrictPiecewiseLinearFunction()` object takes in the first parameter which 
must be the associated `CombCurve()` object, and the dictionary of edge slopes as the second parameter. In the example 
we have just seen, `f` is perhaps not a mesa on `C`, and even more, is perhaps not even well defined!

### Testing the Well - Definedness of Your SPLF <a name="splfDefined"></a>

For the last two conundrums, included in the SPLF class are functions two verify well definedness and also a mesa test.

The first we will discuss is the well definedness test, which is done by the function `assertIsWellDefined()`, which 
can be typed into your testing document in this manner below the definition and declaration of your function:

```
f.assertIsWellDefined()
```

If and when the function (`SPLF`) is not well defined, an error will be raised by the function in your terminal. The 
method by which `assertIsWellDefined()` checks for well definedness is by evaluating path integrals over the loops of 
the graph, as if the function is indeed well defined, each path integral over the loops in the graph will be zero.

### Checking if Your Function is a Mesa <a name="splfMesa"></a>

We now come to one of the most important parts of the SPLF class, which is an attempt to answer the age old question 
that has plagued thinkers from all tropics of tropical geometry, is this SPLF a mesa?

In the class, we have the function `mesaTest` which will (try to) do exactly that.
It is important to note that the SPLF must first be well defined before this test is run, fortunately I am glad to say 
that the `mesaTest` does check to see if the function in question is or is not well defined.

The `mesaTest` is a property, so in this case we enter the function without parentheses:

```
f.mesaTest
```

Much like the previous well-definedness test, this function will raise a value error depending on which portion of the 
definition fails for your function if your function is not a mesa. Included in the function are specific numbers in the
form of print statements to describe which part of the definition your function did not fare well on.

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





## General Families <a name="Families"></a>

1. [Basic Usage](#famBasicUsage)
2. [Classes](#famClasses)

### Basic Usage <a name="famBasicUsage"></a>

### Classes <a name="famClasses"></a>

The classes are as follows:
- [BasicFamilyMorphism](#famMorphClass): Represents a morphism of basic families.
- [Family](#familyClass): Represents a family of tropical curves.
- [TropicalFamily](#tropFamClass): A subclass of `Family` which represents the tropical moduli spaces.
- [PLFFamily](#plfFamily): Represents a piecewise linear function over a family.

#### `BasicFamilyMorphism` <a name="famMorphClass"></a>

A `BasicFamilyMorphism` is a morphism of basic families. It has a domain and codomain, both of which are basic families
(i.e., `CombCurve`s). It also has a morphism of curves and a morphism of monoids.

To do: Example(s)

#### `Family` <a name="familyClass"></a>

A `Family` consists of a collection of basic families and a collection of morphisms between those basic families.

Methods:

- `getAncestors`: Given a basic family `C`, returns the set of all ancestors of `C`. A basic family `F` is an ancestor
of `C` iff the class possesses a morphism from `F` to `C`. 
- `getMaximalCurveIter`: Returns an iterator of all curves / basic families which are not a proper contraction of
another curve in the family.

To do: Example(s)

#### `TropicalFamily` <a name="tropFamClass"></a>

To do: Description

To do: Example(s)

#### `PLFFamily` <a name="plfFamily"></a>

To do: Description

To do: Example(s)