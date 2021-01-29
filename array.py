from array import *
vals = array('i',[5,9,5,3,2])

newARR= array(vals.typecode,(a*a for a in vals))
print(newARR)

n= int(input("Enter the length of array"))
arr= array('i',[])
for k in range(n):
    x= int(input("Enter the value of array"))
    arr.append(x)
    continue
print(arr)
