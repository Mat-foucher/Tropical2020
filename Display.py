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

        self.curveDisplay = nx.MultiDiGraph()

        #self.curveDisplay.add_nodes_from(C.vertices)

        for vert in C.vertices:
            if vert.genus == 0:
                self.curveDisplay.add_node(vert, image="genus_0_vert.png", label="")
            elif vert.genus == 1:
                self.curveDisplay.add_node(vert, image="genus_1_vert.png", label="")
            elif vert.genus == 2:
                self.curveDisplay.add_node(vert, image="genus_2_vert.png", label="")
            else:
                self.curveDisplay.add_node(vert)


        # self.curveDisplay.add_edges_from([(e.vert1, e.vert2) for e in C.edges])
        for e in C.edges:
            numConnections = sum(1 for edge in C.edges if edge.vertices == e.vertices)
            if numConnections > 1 or len(e.vertices) == 1:
                self.curveDisplay.add_node(e, label="", width=0.0, height=0.0)
                self.curveDisplay.add_edge(e.vert1, e, arrowsize=0.0)
                self.curveDisplay.add_edge(e, e.vert2, arrowsize=0.0)
            else:
                self.curveDisplay.add_edge(e.vert1, e.vert2, arrowsize=0.0)

        for leg in C.legs:
            self.curveDisplay.add_node(leg, label="", color="white", width=0.0)
            self.curveDisplay.add_edge(leg.root, leg)

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
            
    def loadSpaceFromFile(self, filename_, saveFilename):
        
        M = TropicalModuliSpace(0,0)
        M.loadModuliSpaceFromFile(filename_)

        modSpaceDisplay = nx.MultiDiGraph()

        counter = 0

        for c in M.curves:
            newDisplayCurve = DisplayCurve(c)
            newDisplayCurve.display("moduliSpaceCurves/Curve" + str(counter) + ".png")
            c.name = counter
            modSpaceDisplay.add_node(c.name, image="moduliSpaceCurves/Curve" + str(counter) + ".png", label="")
            counter = counter + 1 
        
        for key in M.contractionDict:
            for pair in M.contractionDict[key]:
                modSpaceDisplay.add_edge(key.name, pair[1].name)
        
        graph = to_agraph(modSpaceDisplay)
        graph.layout('neato')
        graph.draw(saveFilename)
        
        
        


        



        
        

        
