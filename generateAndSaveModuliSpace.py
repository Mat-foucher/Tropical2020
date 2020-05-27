import sys
from ModuliSpaces import *

if len(sys.argv) != 3:
    print("Usage: python3 generateAndSaveModuliSpace.py g n")
else:
    g = int(sys.argv[1])
    n = int(sys.argv[2])
    m = TropicalModuliSpace(g, n)
    m.generateSpaceDFS()
    m.saveModuliSpaceToFile()