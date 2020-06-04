
class Monoid(object):
	def __init__( m ):
		m.gens = set()
		m.rels = set()

		class Element( object ):
			# elements here mean elements of the associated group

			def __init__( e, coeffs ):
				assert isinstance( coeffs, dict )
				assert coeffs.keys() <= m.gens
				for n in coeffs.values(): assert isinstance(n,int)
				e.monoid = m
				e.coeffs = coeffs
			
			def __add__( self, other ):
				return m.add( self, other )

			def __sub__( self, other ):
				return self.monoid.sub( self, other )
			
			def __rmul__( self, other ):
				return self.monoid.scale( other, self )

			def __eq__( self, other ):
				return self.monoid.eq( self, other )
			
		m.Element = Element

	def addgen( self, gen ):
		self.gens.add( gen )

	def addrel( self, rel ):
		self.rels.add( rel )

	def add( self, x, y ):
		assert isinstance( x, self.Element ) and isinstance( y, self.Element )
		return self.Element({ k : x.coeffs.get(k,0) + y.coeffs.get(k,0) 
				 for k in x.coeffs.keys() | y.coeffs.keys() })

	def sub( self, x, y ):
		return x + (-1)*y
		
	def scale( self, n, x ):
		assert isinstance(n, int) and isinstance( x, self.Element )
		return self.Element({ k : n * x.coeffs[k] for k in x.coeffs.keys() })

	def eq( x, y ):
		# we use Gaussian elimination to determine whether x - y is a relation
		# we work with saturated monoids here, so we can do Gaussian elimination
		# in the associated rational vector space

		z = x - y



