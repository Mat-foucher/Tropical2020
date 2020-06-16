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

The code for this project is divided into separate files, each for different classes that implement objects from the overleaf document.

The different files are:

- StrictPiecewiseLinearFunction.py
- CombinatorialCurve.py
- ModuliSpaces.py
- RPC.py
- tests.py

### Testing <a name="Testing"></a>

The test document is where most of the actual code is used for purposes concerning the research project. 
You may use the tests document for any test you would like to try, using the code from other documents.
In the tests file there is also a large collection of examples from the overleaf document, for example, here is example 3.5:

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

In conclusion, for those picking up this code to use for pioneering things on tropical geometry, most of the work will be done in tests.py

### Combinatorial Curves <a name="CombCurves"></a>

The document CombinatorialCurve.py is for all specifications regarding the combinatorial tropical curves as seen in the overleaf.
In the timeline of this project, the classes in this doc have been modified over and over and over and over again (lowkey kind of painful).

In this current version, the first two classes you will see in this document are the vertex(), edge(), and leg() classes.

Vertex:
    The vertex class specifies the vertex object, which will always need a name (string) and a genus (integer value).
    In this class is a function to set the genus and a property to return the genus of the vertex.
    If we want to declare a nex vertex, we can do so like in this example:

        v1 = vertex("v1", 1)

    Where "v1" is the name of the vertex v1, and v1 has a genus 1.
    NOTE: The genus must always be non-negative, else an error is raised.

Edge:
    The edges are a bit spicier than the vertices, as you may have already guessed.
    For edge objects, each edge has a name in their definition, much like the vertices.
    The edge object also includes a float parameter called length (non-negative, of course), and inputs for TWO vertices.

    NOTE: For "self - edges" on the curve, you can input the same vertex for both positions.

    To create an edge, one writes something like the following:

        e1 = edge("e1", 1.0, v1, v2)
    
    This is an edge with name "e1" or edge one, and e1 has length 1.0 and goes from vertex v1 to vertex v2 (assuming these vertices were previously defined).
    Included in the class definition of edge(), there are a few functions that do what you'd pretty much expect like in vertices, such as getting the length (length()),
    setting the length (length(length_)) and lastly returning the vertices.
    Since this is python 3, we have access to the set() object, an unindexed list. When the function vertices() in edges() is called, this will return a set with two elements:
    the vertices that the edge connects.

### Strict Piecewise Linear Functions <a name="SPLFs"></a>

### Moduli Spaces <a name="ModSpaces"></a>

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
    
#### Members of `TropicalModuliSpace`
    
#### Generating the strata

In order to generate the strata of the moduli space, use the function `generateSpaceDFS`. This function first adds the 
unique `n`-marked stable curve of genus `g` with zero edges to the `curves` member. Then, the program examines which 
strata can be specialized, and adds these specializations to `curves` if they are novel (up to isomorphism).

This process is performed in a depth-first manner: As soon as a curve `C` is specialized to another curve `C'`, the
specializations of `C'` are generated.

#### Generating the contraction information

In order to generate the contraction dictionary of the moduli space, use the function `generateContractionDictionary`.
For each curve `C` in the space, and for each edge `e` of `C`, this function identifies which curve of the space is
isomorphic to the weighted edge contraction `C/{e}`.