source=input("Enter number between 0.0 to 1.0,")
try:
    sc=float(source)
except:
    print("Error Enter Number")
if sc<=0 or sc>=1.0:
    print("Error")
elif sc>=0.9:
    print("A")
elif sc>=0.8:
    print("B")
elif sc>=0.7:
    print("C")
elif sc>=0.6:
    print("D")
elif sc<0.6:
    print("Fail")
quit()
