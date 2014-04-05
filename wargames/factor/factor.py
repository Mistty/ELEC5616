from math import sqrt,ceil
import sys,os
from progressbar import ProgressBar

# Fermat's factorization method, improved with a quadratic siev
n=float(7454122682162520055382580802760182154910553981949204793558856043740374037673027528018697816926025441197656732811124355159939)
a = ceil(sqrt(n))
b2 = a*a-n

c=1
total=n-a
pbar=ProgressBar()
os.system('setterm -cursor off')
while int(sqrt(n))**2!=n:
    a = a + 1
    c = c + 1
    b2 = a*a-n
    count = str(100*c/total)
    sys.stdout.write(count)
    sys.stdout.flush()
    sys.stdout.write('\r')
    sys.stdout.flush()

print (a-sqrt(b2))
print (a+sqrt(b2))
