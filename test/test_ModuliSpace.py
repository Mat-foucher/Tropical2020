
from Tropical2020.general_families.ModuliSpace import *


class ModuliSpaceTests:
    @staticmethod
    def verifyCommonSizes():
        m10 = TropicalModuliSpace(1, 0)
        m10.generateSpaceDFS()
        assert len(m10.curves) == 1

        m11 = TropicalModuliSpace(1, 1)
        m11.generateSpaceDFS()
        assert len(m11.curves) == 2

        m12 = TropicalModuliSpace(1, 2)
        m12.generateSpaceDFS()
        assert len(m12.curves) == 5

        m13 = TropicalModuliSpace(1, 3)
        m13.generateSpaceDFS()
        assert len(m13.curves) == 11

        m14 = TropicalModuliSpace(1, 4)
        m14.generateSpaceDFS()
        assert len(m14.curves) == 30

        m15 = TropicalModuliSpace(1, 5)
        m15.generateSpaceDFS()
        assert len(m15.curves) == 76

        m22 = TropicalModuliSpace(2, 2)
        m22.generateSpaceDFS()
        assert len(m22.curves) == 60


def test_sizes():
    # Generate some small, known, moduli spaces
    ModuliSpaceTests.verifyCommonSizes()
