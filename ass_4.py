def computepay(wh,o,h,r):
    if h>wh:
        overtime=(h-wh)*(r*o)
        work=(h*r)
        total=overtime + work
    else:
        total=h*r
    return total
whours= input("Enter work hours")
hrs = input("Enter Hours:")
rate=input("Enter Rate:")
over=input("Enter overtime rate")
try:
    wh=float(whours)
    o=float(over)
    h=float(hrs)
    r=float(rate)
except:
    print("Enter number")
p = computepay(wh,o,h,r)
print("Pay",p)