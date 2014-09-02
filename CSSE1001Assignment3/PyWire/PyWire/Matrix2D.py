"""
Matrix 2D
@author Scott Hurring [scott at hurring dot com]
	http://hurring.com/code/python/matrix2d/
@version v0.3 - Apr 20, 2006

A simple 2-dimensional Matrix class for 2d matrix operations.

I wrote this code to help with my Linear Algebra homework one night
and then reworked it a few months later to take better advantage
of closures and lambda funcs.

The purpose of this code was to help me understand linear
algebra better and brush up on my python skills... this code was
not written for speed or optimization, so please beware that
there are probably much faster/better ways of computing things
than i do here...

@examples

from Matrix2D import *

# Construct a 3x5 matrix
M = Matrix2D.create(3,5)
# Construct a 5x5 identity matrix
I = Matrix2D.identity(5,5)

# Multiply A times B
A = Matrix2D.fromlist(2, [1,2, 3,4])
B = Matrix2D.fromlist(2, [4,3, 2,1])
C = A * B		# equivalent to: C = A.multiply(B)
print C.tolist()	# [[8, 5], [20, 13]]
assert C.tolist() == [[8, 5], [20, 13]]

# Prove inverse
I = B / B		# eqiv to: I = B * B.inverse()
assert B / B == Matrix2D.identity(2,2)

# Multiply by scalar 2
A.apply_lambda( lambda x: x*2 )
print A.tolist()	# [[2,4], [6,8]]
assert A.tolist() == [[2,4], [6,8]]

# Round everything to 2 decimal places
A.apply_lambda( lambda x: round(x, 2) )

# Blank the diagonal with 0's
# leave everything else untouched
def f(row,col, value):
	if (row==col): return 0
A.apply_func(f)
print A.tolist()	# [[0,4], [6,0]]
assert A.tolist() == [[0,4], [6,0]]

# Get the dot-product of two vectors (at * b)
a = Matrix2D.vector([1,2,3])
b = Matrix2D.vector([3,2,1])
c = a.t() * b
print c.toscalar()	# 10
assert c.toscalar() == 10

# Get dot product of A.row1 and B.col1
c = A.get_row(0) * B.get_col(0) 
print c.toscalar()	# 8
assert c.toscalar() == 8.0	
	
"""

class MatrixException(Exception):
	pass
	
class Matrix2D(object):
	"""
	Simple class for representing and working with 2D matrixes.
	"""
	dbg = 0
	A = []
	dim = [0,0]
	
	def __init__(self, matrix):
		self.rows = len(matrix)
		self.cols = len(matrix[0])
		self.dim = [self.rows, self.cols]
		self.setlist(matrix)

	#############################################################
	# Static constructor methods
		
	def create(rows,cols, value=0):
		"""
		Create a matrix.
		"""
		matrix = []
		for row in range(rows):
			matrix.insert(row, [])
			for col in range(cols):
				matrix[row].insert(col, value)
		return Matrix2D(matrix)

	def ones(rows,cols):
		return Matrix2D.create(rows,cols, 1.0)

   	def zeros(rows,cols):
		return Matrix2D.create(rows,cols, 0.0)

	def identity(rows,cols):
		M = Matrix2D.create(rows,cols, 0.0)
		def f(row,col, value):
			if row == col: return 1.0
		M.apply_func(f)
		return M
		
	def clone(self):
		return Matrix2D(self.tolist())

	def fromlist(cols, values):
		rows = len(values) / cols
		matrix = []
		for row in range(rows):
			matrix.insert(row, [])
			for col in range(cols):
				value = values[(cols*row)+col]
				matrix[row].insert(col, value)
		return Matrix2D(matrix)

	def vector(vector):
		return Matrix2D.fromlist(1, vector)
		
	create = staticmethod(create)
	ones = staticmethod(ones)
	zeros = staticmethod(zeros)
	identity = staticmethod(identity)
	fromlist = staticmethod(fromlist)
	vector = staticmethod(vector)

	##################################################################
	# Transform the matrix into another representation
	
	def tolist(self):
		return self.A[:]
		
	def toscalar(self):
		"""Return 0d scalar"""
		return self.A[0][0]
		
	def tovector(self):
		"""Return a 1d list of the first column (vector)"""
		return self.get_col(0).t().tolist().pop()
		
	def tomatrix(self):
		"""Return 2d list of the whole matrix (matrix)"""
		return self.clone()
					
	##################################################################
	# Work with this matrix
	
	def get(self, row,col):
		"""
		Return an element from the matrix
		"""
		return self.A[row][col]

	def set(self, row,col, value):
		"""
		Set an element of the matrix.
		"""
		self.A[row][col] = value
		
	def set_all(self, value):
		"""
		Set all elements of this matrix to value
		"""
		for row in range(self.rows):
			for col in range(self.cols):
				self.set(row,col, value)
				
	def setmatrix(self, B):
		self.A = B.tolist()

	def setlist(self, matrix):
		"""Set the entire matrix in one shot"""
		self.A = matrix[:]
		
	def get_col(self, col):
		"""Get a column as a matrix"""
		return Matrix2D.fromlist(1, self.get_col_tolist(col))

	def get_col_tolist(self, col):
		return [ self.A[i][col] for i in range(self.rows) ]

	def get_row(self, row):
		"""Get a row as a matrix"""
		return Matrix2D([self.get_row_tolist(row)])
	
	def get_row_tolist(self, row):
		return self.A[row]

	####################################################################
	# Iterate through this matrix
	
	def walk(self):
		"""
		Walk through all elements.
		"""
		for row in range(self.rows):
			for col in range(self.cols):
				yield(row,col)
				
	def walk_cols(self):
		for col in range(self.cols):
			yield self.get_col(col)
				
	def walk_rows(self):
		for row in range(self.rows):
			yield self.get_row(row)			
			
	##################################################################
	# Operations with another matrix
	# A op B -> C
	
	def __eq__(self, B): return self.equal(B)
	def equal(self, B):
		for (row,col) in self.walk():
			# round so that: 0.00000000001 == 0
			a = round(self.get(row,col),5)
			b = round(B.get(row,col), 5)
			if a != b:
				#print a, "!=", b, " == False"
				return False
		#print "== True"
		return True
		
	def __add__(self, B): return self.add(B)
	def add(self, B):
		"""
		Add this matrix to another. C=A+B
		"""
		(m,n) = B.dim

		if m != self.rows or n != self.cols:
			raise MatrixException("add: Invalid dimensions (%i,%i)" % (m,n))

		C = Matrix2D.create(m,n)
		def f(row,col, value):
			return self.get(row,col)+B.get(row,col)	
		C.apply_func(f)
		
		return C

	def __mul__(self, B): return self.multiply(B)
	def multiply(self, B):
		"""
		Multiply this matrix against another. C=AB
		"""
		m = self.rows
		(n, l) = B.dim

		if n != self.cols:
			raise MatrixException("multiply: Invalid dimensions (%i,%i)" % (n,l))
			
		C = Matrix2D.create(m,l)
		def f(row,col, value):
			return self.dot(B, row,col)
		C.apply_func(f)
		
		return C
		
	def __div__(self, B): return self * B.inverse()

	####################################################################
	# Options on this matrix that return a new matrix
	# A.op() -> B
	
	def inv(self): return self.inverse()
	def inverse(self):
		"""
		Compute and Return the Gauss-Jordan inverse of this matrix. A->A^-1
		"""
		self.debug("Inverse", 1)
		B = self.append_identity()
		B.reduce()
		B = B.unshift_identity()
		return B

	def reduce(self):
		"""
		Reduce to 'reduced echelon' form.  A->R
		"""
		self.debug("Reduce", 1)
		#B = self.clone()
		self.upper_triangular()
		self.pivots_to_1()
		self.lower_triangular()

	def t(self): return self.transpose()
	def transpose(self):
		"""
		Transpose this matrix.  A->At
		"""
		self.debug("Transpose", 1)
		M = Matrix2D.create(self.cols, self.rows)
		
		def f(row,col, value):
			return self.get(col, row)
		M.apply_func(f)
		
		# replaced with apply_func code
		#for row in range(self.rows):
		#	for col in range(self.cols):
		#		B.set(col,row, self.get(row,col))
		
		self.debug(M.tolist(), 2)
		return M
		
	def append_identity(self):
		"""
		Return new matrix with identity appended on end. 
		Used to find inverse
		A -> [A I]
		"""
		self.debug("Append identity", 1)
		M = Matrix2D.create(self.rows,self.cols*2)
		
		def f(row,col, value):
			if col >= self.cols: return (int)(row==col-self.cols)
			else: return self.get(row,col)
		M.apply_func(f)
				
		self.debug(M.tolist(), 2)
		return M
		
	def unshift_identity(self):
		"""
		Return this matrix without the identity matrix in front.
		Used after finding inverse.
		[I A] -> A
		"""
		self.debug("Unshift identity", 1)
		cols = self.cols / 2
		M = Matrix2D.create(self.rows,cols)
		I = Matrix2D.create(self.rows,cols)
		
		for row in range(self.rows):
			for col in range(cols):
				I.set(row,col, self.get(row,col))
				M.set(row,col, self.get(row,col+cols))
				
		if not I == Matrix2D.identity(self.rows,cols):
			raise Exception("Expected identity at front, but found ", I.tolist())

		self.debug(M.tolist(), 2)
		return M

	##################################################################
	# Functions that mutate this matrix in-place

	def upper_triangular(self):
		"""
		Put this matrix into upper-triangular form.
		Go TOP->BOTTOM, eliminating all numbers UNDER pivots.
		"""
		self.debug("Upper triangular", 1)
		self.debug(self.A, 2)
		(m, n) = (self.rows, self.cols)
		# For each pivot
		for i in range(m-1):
			pivot = self.get(i,i)
			# Skip pivots that are "0"
			if pivot == 0: continue

			# For each row underneath this pivot
			for j in range(i+1,m):
				if self.get(j,i) == 0: continue
				mult = -1.0 * (1.*self.get(j,i)) / (1.*pivot)
				# If this is non-zero below a pivot
				self.subtract_row(mult, i, j)
		self.debug(self.tolist(), 2)
		
	def lower_triangular(self):
		"""
		Put this matrix into lower-triangular form.
		Go BOTTOM->TOP eliminating all numbers ABOVE pivots.
		"""
		self.debug("Lower triangular")
		(m, n) = (self.rows, self.cols)
		for i in range(m-1, 0, -1):
			pivot = self.get(i,i)
			# Skip pivots that are "0"
			if pivot == 0: continue

			# For each row above this pivot
			for j in range(i-1, -1, -1):
				if self.get(j,i) == 0: continue
				mult = -1.0 * (1.*self.get(j,i)) / (1.*pivot)
				# If this is non-zero above a pivot
				self.subtract_row(mult, i, j)
				#self.output()
		self.debug(self.tolist(), 2)

	def pivots_to_1(self):
		"""
		Divide entire row by pivot to set pivot=1.
		"""
		self.debug("Pivots to 1")
		(m, n) = (self.rows, self.cols)
		for i in range(m):
			pivot = self.get(i,i)
			if pivot == 0: break
			for c in range(n):
				v = (1.*self.get(i,c)) / (1.*pivot)
				#print "pivot=",pivot, "v=", 1.0*self.get(i,c), "/", 1.*pivot, "=", v
				self.set(i,c, v)
		self.debug(self.tolist(), 2)

	def subtract_row(self, mult, i,j):
		"""
		Subtract (row i)*mult from (row j)
		or: (row j) + (row i)*(-mult).
		"""
		self.debug("Subtract pivot ([%i][%i] mult=%0.4f)" % (i,j,mult))

		# Muliplier_row = Pivot_row * mult
		mrow = []
		for c in range(self.cols):
			mrow.insert(c, self.get(i,c)*mult)

		#print "[",i,"][",i,"] [",j,"] row=", self.get(j,i) ,"; mult=",mult, " :: ", mrow

		# Now subtract mrow from A[row+1]
		for c in range(self.cols):
			v = self.get(j,c)+mrow[c]
			#print self.get(j,c), "+", mrow[c], "=", v
			self.set(j,c, v)

		self.debug(self.tolist(), 2)
		
	def apply_func(self, func):
		"""
		Apply a function to every element in this matrix.
		if func returns None, the value is left unchanged
		if func returns a value, the value is set to it
		func = f(row,col, value)
		"""
		for (row,col) in self.walk():
			fvalue = func(row,col, self.get(row,col))
			if fvalue != None:
				self.set(row,col, fvalue)
				
	def apply_lambda(self, func):
		"""
		Apply a simple lambda to every element in this matrix.
		The element's value is set to the return of the lambda 
		func = lambda value: ...	
		"""
		for (row,col) in self.walk():
			self.set(row,col, func(self.get(row,col)))
					
	####################################################################
	# Helper / cleanup  functions
	
	def round(self, n=2):
		f = lambda x: round(x, n)
		self.apply_lambda(f)
		
	def cleanup(self):
		def f(row,col, value):
			# removes "-0.00"
			if not value: return 0		#abs(value)
			return round(value, 2)
		self.apply_func(f)
		
	##################################################################
	# Debug, output, etc... 
	
	def __str__(self):
		s = "Matrix(%i,%i):\n" % (self.rows, self.cols)
		for row in self.walk_rows():
			row = row.tolist()[0]
			row = [ "%10.2f" % row[i] for i in range(len(row)) ]
			s = s + "[" + " | ".join(row) + " ]\n"
		return s
			
	def debug(self, text, level=3):
		if self.dbg >= level: print text
#
#






## 	def dot(self, B, i=1, j=1):
## 		"""
## 		Dot product of 1xn and nx1 vectors
## 		"""
## 		At = self.transpose()
## 		C = At.summate(B)
	
	def dot(self, B, i=0,j=0):
		"""
		Dot product of *self* row 'i' and *B* column 'j'
		Sum (for k=range(B.rows) of: A[i][k]*B[k][j]
		scalar = A(row i) dot B(col j)
		"""
		value = 0
		for k in range(B.rows):
			#print "value +=A[%i][%i] * B[%i][%i]" % (i,k, k,j)
			value += self.get(i,k) * B.get(k,j)
		return value

