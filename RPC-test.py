from RPC import *

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
