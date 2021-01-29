smallest=None
largest=None
while True:
    try:
        num = input("Enter a number:")
        if num == 'done':
            break

    except:
        print("Invalid input")


number=num(float)
for x in number:
    if largest is None:
        largest=x
    elif largest>x:
        largest=x
print("Maximum is",largest)
for x in number:
    if smallest is None:
        smallest=x
    elif smallest<x:
        smallest=x
print("Minimum is",smallest)