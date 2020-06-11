
import math
import itertools
import copy

def gcd( a, b ):
	while a:
		a, b = b, a % b
	return b

def lcm( a, b ):
	return a*b/gcd(a,b)

class Monoid(object):
	def __init__( m ):
		m.gens = list()		# must store as a list so iterations 
							# are always in the same order

		m.rels = dict()		# a dictionary indexed by elements of m.gens
							# consists of relations in row echelon form

		m.dual = None

		class Element( object ):
			# elements here mean elements of the associated group

			def __init__( e, coeffs, d=1 ):
				assert isinstance( d, int )
				assert isinstance( coeffs, dict )
				for x in coeffs.keys(): assert x in m.gens
				for n in coeffs.values(): assert isinstance(n,int)
				e.monoid = m
				e.coeffs = coeffs
				e.denom = d
			
			def __add__( self, other ):
				return m.add( self, other )

			def __iadd__( self, other ):
				return m.iadd( self, other )

			def __isub__( self, other ):
				return m.isub( self, other )

			def __sub__( self, other ):
				return m.sub( self, other )

			def __itruediv__( self, d ):
				return m.idiv( self, d )

			def __truediv__( self, d ):
				return m.div( self, d )

			def __floordiv__( self, other ):
				return m.floordiv( self, other )

			def __ifloordiv__( self, d ):
				return m.ifloordiv( self, d )

			def __imul__( self, other ):
				return m.iscale( other, self )
			
			def __rmul__( self, other ):
				return m.scale( other, self )

			def __eq__( self, other ):
				return m.eq( self, other )

			def __getitem__( self, key ):
				return self.coeffs.get(key, 0)

			def copy( self ):
				return m.Element( dict(self.coeffs), self.denom )

			def scalereduce( self ):
				return m.scalereduce( self )
			
		m.Element = Element

	def zero( self ):
		return self.Element( { } )


	def addgen( self, gen ):
		self.gens.append( gen )

	def addrel( self, rel ):
		for x in self.gens:
			if x in self.rels.keys():
				# if there is already a relation with an x coefficient,
				# subtract a multiple of that relation to make sure this
				# relation is in reduced echelon form
				rel = self.rels[x][x]*rel - rel[x]*self.rels[x]
			elif rel[x] != 0:
				# there is no relation with an x coefficient, and this
				# relation's x coefficient is nonzero, so it is in echelon form
				# and we can add it
				d = 0
				for v in rel.coeffs.values(): d = math.gcd(d,v)
				self.rels[x] = rel // d
				break

	def compute_dual( M ):
		if M.dual: return M.dual

		M.dual = set()

		basis = [ x for x in M.gens if x not in M.rels.keys() ]
		dim = len(basis)
		if dim == 0:
			return

		reducedgens = { x : M.Element({x:1}).scalereduce() for x in M.gens }
		pivots = dict()

		# every set of dim(M)-1 elements gives a linear function
		for T in itertools.combinations(M.gens, dim-1):
			pivots = dict()
			# put the elements of T in RREF
			for x in T:
				v = reducedgens[x].copy()
				M.scalereduce( v, pivots )
				pivots[next(y for y in basis if v[y])] = v
			
			# the basis element without a pivot
			lastcol = next(y for y in basis if y not in pivots)

			def F( v, pivots=pivots ): # this is the linear function
				# v is an M.Element
				# we put v in RREF relative to T

				w = v.copy()
				M.scalereduce( w )
				M.scalereduce( w, pivots )

				return w[lastcol] if w.denom >= 0 else -w[lastcol]

			if all( [ F(M.Element({x:1})) >= 0 for x in M.gens ] ):
				M.dual.add( F )
			elif all( [ F(M.Element({x:1})) <= 0 for x in M.gens ]):
				M.dual.add( lambda v : -F( v ) )


	def add( self, x, y ):
		assert isinstance( x, self.Element ) and isinstance( y, self.Element )
		return self.Element( 
				{ k : y.denom * x.coeffs.get(k,0) + x.denom * y.coeffs.get(k,0) 
					for k in x.coeffs.keys() | y.coeffs.keys() }, 
				x.denom * y.denom 
			)

	def iadd( self, x, y ):
		for k in y.coeffs.keys():
			x.coeffs[k] = y.denom * x.coeffs.get(k,0) + x.denom * y.coeffs[k]
		return x

	def isub( self, x, y ):
		for k in y.coeffs.keys():
			x.coeffs[k] = y.denom * x.coeffs.get(k,0) - x.denom * y.coeffs[k] 
		return x

	def sub( self, x, y ):
		return x + (-1)*y
		
	def floordiv( self, x, y ):
		return self.Element( { k : x.coeffs.get(k,0)//y 
							   for k in x.coeffs.keys() } )

	def ifloordiv( self, d ):
		for x in self.coeffs: self.coeffs[x] //= d
		return self
		
	def scale( self, n, x ):
		assert isinstance(n, int) and isinstance( x, self.Element )
		return self.Element( { k : n * x.coeffs[k] for k in x.coeffs.keys() } )

	def iscale( self, n, x ):
		for k in x.coeffs.keys():
			x.coeffs[k] *= n
		return x

	def idiv( self, x, d ):
		x.denom *= d
		return x

	def div( self, x, d ):
		y = x.copy()
		y.denom *= d
		return y

	def reduce_fraction( self ):
		d = x.denom
		for c in x.coeffs.values():
			d = gcd(c,d)
		x.denom /= d
		x //= d

	def scalereduce( self, z, rels=None ):
		if rels == None: rels = self.rels
		for w in rels.keys():
			a = z[w]
			z *= rels[w][w]
			z -= a * rels[w]
			z.denom *= rels[w][w]
		return z

	def eq( self, x, y ):
		# we use Gaussian elimination to determine whether x - y is a relation
		# we work with saturated monoids here, so we can do Gaussian elimination
		# in the associated rational vector space
		# the relations are already known to be in row echelon form

		z = x - y
		z.scalereduce()
		return not all(z.coeffs.values())

	def isgeqzero( M, x ):
		L = [ F(x) for F in M.dual ] 
		return all(L)
