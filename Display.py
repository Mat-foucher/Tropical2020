import networkx as nx 
from ModuliSpaces import *
from numpy import *
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

        self.name = C.name
        
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
    
    def addDisplay(self, displayCurve):
        self.displays.add(displayCurve)
        print("Display", displayCurve.name, "has been added to", self.name)

    def showAllDisplays(self, name_):
        
        displaysToShow = set()

        for i in self.displays:
            displaysToShow.add(i)
        
        plot = to_agraph()

        plot.add_nodes_from(displaysToShow)

        plot.layout('neato')

        plot.draw(name_)
            
    def loadSpaceFromFile(self, filename_):
        
        M = TropicalModuliSpace(0,0)
        M.loadModuliSpaceFromFile(filename_)

        modSpaceDisplay = nx.MultiDiGraph()

        counter = 0

        for c in M.curves:
            newDisplayCurve = DisplayCurve(c)
            newDisplayCurve.display("moduliSpaceCurves/Curve" + str(counter) + ".png")
            c.name = counter
            modSpaceDisplay.add_node(c.name, image="moduliSpaceCurves/Curve" + str(counter) + ".png")
            counter = counter + 1 
        
        for key in M.contractionDict:
            for pair in M.contractionDict[key]:
                modSpaceDisplay.add_edge(key.name, pair[1].name)
        
        graph = to_agraph(modSpaceDisplay)
        graph.layout('dot')
        graph.draw("renderedModSpaces/example.png")
        
        
        


        



        
        

        
