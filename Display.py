import networkx as nx 
from networkx.drawing.nx_agraph import to_agraph
import matplotlib.pyplot as plt
from CombinatorialCurve import *

class DisplayCurve(object):
    def __init__(self, C):
        self.curve = C
        self.vertices = set()
        self.edges = set()

        self.curveDisplay = nx.MultiGraph()

        self.curveDisplay.add_nodes_from(C.vertices)

        self.curveDisplay.add_edges_from([(e.vert1, e.vert2) for e in C.edges])
        
    @property
    def getEdges(self):
        if len(self.curveDisplay.edges) > 0:
            return self.curveDisplay.edges
        else:
            print("WARNING: No edges in display curve!")
            return set()

    @property
    def getVertices(self):
        if len(self.curveDisplay.vertices) > 0:
            return self.curveDisplay.vertices
        else:
            print("WARNING: No verticies in display curve!")
            return set()
        
    def display(self, name_):
        A = to_agraph(self.curveDisplay) 
        A.layout('neato')                                                                 
        A.draw(name_)

class Display(object):
    def __init__(self, name_, displays_):

        self.name = name_
        self.displays = displays_
    
    