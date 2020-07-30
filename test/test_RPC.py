from Tropical2020.basic_families.RPC import *
import pdb

def test_RPC():

	X = "x"
	Y = "y"
	M = Monoid([X,Y])

	x = M.Element({X:1})
	y = M.Element({Y:1})

	assert not M.eq(x,y)

	N = M.extend(rels=[x-y])

	F = MonoidHomomorphism(M,N)	
	
	assert N.eq(F(x),F(y))


	P = Monoid([1,2,3],[{1:1,2:1,3:-2}])
	x = P.Element({1:1})
	y = P.Element({2:1})
	z = P.Element({3:1})


	w = y - x
