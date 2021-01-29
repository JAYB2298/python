for i in range(4):
   for j in range(i+1):
     print("*",end="")
   print()

print("another")
for i in range(4):
   for j in range(4-i):
     print("*",end="")
   print()

from array import *

vals=array('i',[])