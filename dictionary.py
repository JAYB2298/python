f=open('C:/Users/user 10/Desktop/my documents/data sceince/sample.txt')

di=dict()
for lin in f:
    lin=lin.rstrip()
    wds=lin.split()
    for w in wds:
        di[w]=di.get(w,0)+1
#print(di)

#meethod using list
temp=list()
for k,v in di.items():
    s=(v,k)
    temp.append(s)

temp=sorted(temp,reverse=True)

for v,k in temp[:5]:
    print(k,v)

## method using dictionary
largest= -1
word= None

for k,v in di.items():
    #print(k,v)
    if v > largest:
        largest = v
        word = k
print("largest word is :",word,"\nCount:",largest)
