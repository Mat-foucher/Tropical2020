# Tropical2020
Classifying Tropical Surfaces Research Summer 2020 - CU Boulder

====================================
What is the code, and how to use it:
====================================

The code for this project is divided into separate files, each for different classes that implement objects from the overleaf document.

The different documents (currently) are:

- StrictPiecewiseLinearFunction.py
- CombinatorialCurve.py
- ModuliSpaces.py
- RPC.py
- tests.py

========
tests.py
========

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

=====================
CombinatorialCurve.py
=====================

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

    To declare an edge, one writes something like the following:

        e1 = edge("e1", 1.0, v1, v2)
    
    This is an edge with name "e1" or edge one, and e1 has length 1.0 and goes from vertex v1 to vertex v2 (assuming these vertices were previously defined).
    Included in the class definition of edge(), there are a few functions that do what you'd pretty much expect like in vertices, such as getting the length (length()),
    setting the length (length(length_)) and lastly returning the vertices.
    Since this is python 3, we have access to the set() object, an unindexed list. When the function vertices() in edges() is called, this will return a set with two elements:
    the vertices that the edge connects.