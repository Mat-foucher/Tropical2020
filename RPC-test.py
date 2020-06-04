from RPC import *

M = Monoid()
X = "x"
Y = "y"
M.addgen(X)
M.addgen(Y)
x = M.Element({X:1})
y = M.Element({Y:1})
