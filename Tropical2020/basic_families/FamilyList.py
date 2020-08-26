#from .BasicFamily import *
from .RPC import *

class FamilyList(object):
    def __init__(self, _BasicFamily, _Monoid, _SlopeDictionary, _LegLengthVector):
        self.BasicFamily_ = _BasicFamily
        self.Monoid_ = _Monoid
        self.SlopeDictionary = _SlopeDictionary
        self.LegLengthVector = _LegLengthVector

    @property
    def BasicFamily(self):
        return self.BasicFamily_

    @property
    def Monoid(self):
        return self.Monoid_

    def AssignLengthsToEdges(self, dict_):
        for i in dict_:
            assert dict_[i].is_integer()