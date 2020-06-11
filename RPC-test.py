from RPC import *
import pdb

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


M = Monoid()
M.addgen(1)
M.addgen(2)
M.addgen(3)
x = M.Element({1:1})
y = M.Element({2:1})
z = M.Element({3:1})
M.addrel(x + y - 2 * z)


M.compute_dual()


w = y - x
