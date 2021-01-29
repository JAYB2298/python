smallest=None
greatest=None
while True:
    number=input("Enter any number or write done:")
    if number =="done":
        break
    try:
        number=int(number)
    except:
        print("Invalid input")
        continue
    if (smallest==None) or (smallest>number):
        smallest=number
    if (greatest == None)or (greatest < number):
        greatest=number
print("Maximum is:",greatest)
print("Minimum is:",smallest)
