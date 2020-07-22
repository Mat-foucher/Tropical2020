from Tropical2020.basic_families.RPC import *
import pdb

def test_RPC():

    M = Monoid()
    X = "x"
    Y = "y"
    M.addgen(X)
    M.addgen(Y)
    x = M.Element({X:1})
    y = M.Element({Y:1})

    assert not M.eq(x,y)

    M.addrel(x-y)

    assert M.eq(x,y)


    P = Monoid()
    P.addgen(1)
    P.addgen(2)
    P.addgen(3)
    x = P.Element({1:1})
    y = P.Element({2:1})
    z = P.Element({3:1})
    P.addrel(x + y - 2 * z)


    P.compute_dual()


    w = y - x
