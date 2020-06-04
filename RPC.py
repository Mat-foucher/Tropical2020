
import math

class Monoid(object):
	def __init__( m ):
		m.gens = list()		# must store as a list so iterations 
							# are always in the same order
		m.rels = dict()		# a dictionary indexed by elements of m.gens
							# consists of relations in row echelon form

		class Element( object ):
			# elements here mean elements of the associated group

			def __init__( e, coeffs ):
				assert isinstance( coeffs, dict )
				for x in coeffs.keys(): assert x in m.gens
				for n in coeffs.values(): assert isinstance(n,int)
				e.monoid = m
				e.coeffs = coeffs
			
			def __add__( self, other ):
				return m.add( self, other )

			def __sub__( self, other ):
				return m.sub( self, other )

			def __floordiv__( self, other ):
				return m.div( self, other )
			
			def __rmul__( self, other ):
				return m.scale( other, self )

			def __eq__( self, other ):
				return m.eq( self, other )

			def __getitem__( self, key ):
				return self.coeffs.get(key, 0)
			
		m.Element = Element

	def zero( self ):
		return self.Element( { } )

	def addgen( self, gen ):
		self.gens.append( gen )

	def addrel( self, rel ):
		for x in self.gens:
			if x in self.rels.keys():
				rel = self.rels[x][x]*rel - rel[x]*self.rels[x]
			elif rel[x] != 0:
				d = 0
				for v in rel.coeffs.values(): d = math.gcd(d,v)
				self.rels[x] = rel // d
				break

	def add( self, x, y ):
		assert isinstance( x, self.Element ) and isinstance( y, self.Element )
		return self.Element({ k : x.coeffs.get(k,0) + y.coeffs.get(k,0) 
				 			  for k in x.coeffs.keys() | y.coeffs.keys() })

	def sub( self, x, y ):
		return x + (-1)*y
		
	def div( self, x, y ):
		return self.Element({ k : x.coeffs.get(k,0)//y 
							  for k in x.coeffs.keys() })
		
	def scale( self, n, x ):
		assert isinstance(n, int) and isinstance( x, self.Element )
		return self.Element({ k : n * x.coeffs[k] for k in x.coeffs.keys() })

	def eq( self, x, y ):
		# we use Gaussian elimination to determine whether x - y is a relation
		# we work with saturated monoids here, so we can do Gaussian elimination
		# in the associated rational vector space

		z = x - y
		for w in self.rels.keys():
			z = self.rels[w][w]*z - z[w]*self.rels[w]
		return not all(z.coeffs.values())


