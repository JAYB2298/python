hours=input("Enter hours")
rate=input("Enter rate")
try:
    hr=float(hours)
    r=float(rate)
except:
    print("Enter number")
if hr>40:
    overtime=(hr-40)*(r*0.5)
    work=(hr*r)
    total=work+overtime
else:
    total=hr*r
print(total)
