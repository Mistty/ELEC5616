from Decimal import *
from sys import argv,exit
from multiprocessing import Pool

# Method: Add square numbers to n until it is a perfect square
#        pq  = n
# (a+b)(a-b) = n
# a^2 - b^2  = n
#       a^2  = n + b^2
# p = (a+b), q = (a-b)
# so a is like the "center" and b is the "offset"

def find_ab(c,a):
    b = c.sqrt(c.subtract(c.power(a,2),n))
    while int(b) != b:
	print "Trying a=",a
	print "So the offset must be b=",b
	print "But that is not an integer"
	print ""
	a = c.add(a, 1)
	b = c.sqrt(c.subtract(c.power(a,2),n))
    # so now b is an integer
    print "Trying a=",a
    print "So the offset must be b=",b
    print "b is an integer. STOP"
    print ""
    print "p and q are:"
    print c.add(a,b)
    print c.subtract(a,b)
    print "pq =",c.multiply(a,b)
    print " n =",n
    print "n = pq:",c.multiply(a.b)==n
    exit("Done!")


n = argv[0]			# Get n
c = Context(prec=600)		# Create a precise decimal environment
n = c.create_decimal(n)		# Make python see n as precise
s = int(c.sqrt(n))+1		# Start at the sqrt
a = []
for i in range(1,9):
    a.append(int(str(int(str(s)[0])+i) + str(s)[1:])) # increment the first number of s by i
pool = Pool(processes=8)	# Set up 8 starting points
pool.map(find_ab,a)

