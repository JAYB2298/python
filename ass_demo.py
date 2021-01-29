filename=open('C:/Users/user 10/Desktop/file.txt','r')
f=filename.readlines()
count=0
for x in f:
  if x.startswith('java'):
     count = count + 1
print('line count:',count)
print(x)