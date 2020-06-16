# Tropical2020
Classifying Tropical Surfaces Research Summer 2020 - CU Boulder

## Contents:

1. [Introduction](#Introduction)
2. [Testing](#Testing)
3. [Combinatorial Curves](#CombCurves)
4. [Strict Piecewise Linear Functions](#SPLFs)
5. [Moduli Spaces](#ModSpaces)

### Introduction <a name="Introduction"></a>

#### What is the code, and how to use it:

The code for this project is divided into separate files, each for different classes that implement objects from the 
overleaf document.

The different files are:

- StrictPiecewiseLinearFunction.py
- CombinatorialCurve.py
- ModuliSpaces.py
- RPC.py
- tests.py

### Testing <a name="Testing"></a>

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

### Combinatorial Curves <a name="CombCurves"></a>

1. [Vertices](#vertices)
2. [Edges](#edges)

The document `CombinatorialCurve.py` is for all specifications regarding the combinatorial tropical curves as seen in 
the overleaf document.
In the timeline of this project, the classes in this doc have been modified over and over and over and over again 
(lowkey kind of painful).

In this current version, the first two classes you will see in this document are the `vertex`, `edge`, and `leg` 
classes.

#### Vertices <a name="vertices"></a>

The `vertex` class specifies the vertex object, which will always need a name (`string`) and a genus (`int` value).
In this class is a function to set the genus and a property to return the genus of the vertex.
If we want to declare a nex vertex, we can do so like in this example:

        v1 = vertex("v1", 1)

Where `"v1"` is the name of the vertex `v1`, and `v1` has a genus 1.
NOTE: The genus must always be non-negative, else an error is raised.

#### Edges <a name="edges"></a>

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
    The leg object is much like edge, except for the fact that the leg object can only be assigned a singe vertex that it is connected to.
    Unlike the other graph objects too, the leg does not have any length or genus, making it the simplest class in the file.

    To create a new leg, this can be done so by the following:

        l1 = leg("l1", v1)
        

Neat Example:
======================================================
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

### Strict Piecewise Linear Functions <a name="SPLFs"></a>

### Moduli Spaces <a name="ModSpaces"></a>

1. [Basic Usage](#modSpaceUsage)
2. [Members of `TropicalModuliSpace`](#modSpaceMembers)
3. [Generating the Strata](#modSpaceStrataGen)
4. [Generating the Contraction Dictionary](#modSpaceContractionGen)
5. [Saving and Loading Spaces](#modSpaceIO)

#### Basic Usage <a name="modSpaceUsage"></a>

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
    
#### Members of `TropicalModuliSpace` <a name="modSpaceMembers"></a>

- `curves`: A `Set[CombCurve]` to store the strata of the space.
- `curvesDict`: A `Dictionary[Int, CombCurve]` organizing the strata by their number of edges.
- `contractionDict`: A `Dictionary[CombCurve, List[(Edge, Int)]]` recording the contraction information of the
space. Given a curve `C`, `contractionDict[C]` is a list of elements of the type `(Edge, Int)`. An element `(e, id)`
belongs to `contractionDict[C]` if and only if contracting edge `e` of `C` produces the curve with I.D. `id`.
    
#### Generating the Strata <a name="modSpaceStrataGen"></a>

In order to generate the strata of the moduli space, use the function `generateSpaceDFS`. This function first adds the 
unique `n`-marked stable curve of genus `g` with zero edges to the `curves` member. Then, the program examines which 
strata can be specialized, and adds these specializations to `curves` if they are novel (up to isomorphism).

This process is performed in a depth-first manner: As soon as a curve `C` is specialized to another curve `C'`, the
specializations of `C'` are generated.

#### Generating the Contraction Information <a name="modSpaceContractionGen"></a>

In order to generate the contraction dictionary of the moduli space, use the function `generateContractionDictionary`.
For each curve `C` in the space, and for each edge `e` of `C`, this function identifies which curve of the space is
isomorphic to the weighted edge contraction `C/{e}`.

#### Saving and Loading Spaces <a name="modSpaceIO"></a>

In order to load a moduli space from a file, initialize the space with proper genus and marking number, and then call 
`loadModuliSpaceFromFile(filename)`. To save a space, call `saveModuliSpaceToFile`. Both functions accept delimiter
and encoding information. By default, the curve entry delimiter is `=` and the encoding is `utf-8`. 
`saveModuliSpaceToFile` accepts an optional filename to save to. If none is provided, a filename is automatically
generated based on the genus and marking of the space.

