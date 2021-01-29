f=open('C:/Users/user 10/Desktop/my documents/data sceince/sample.txt')
counts=dict()

for line in f:
    words=line.split()
    for word in words:
        counts[word]=counts.get(word,0)+1
## first method
lst=list()
for c,k in counts.items():
    newup=(k,c)
    lst.append(newup)

lst=sorted(lst,reverse=True)

for val,key in lst[:5 ]:
    print(key,val)

## Second meethod
print(sorted([(v,k) for k,v in counts.items()]))
