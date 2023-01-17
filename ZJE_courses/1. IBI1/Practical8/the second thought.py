import re
a=open('Saccharomyces_cerevisiae.R64-1-1.cdna.all.fa')
file=a.readlines()
a.close()
list=[]
list2=[]
list3=[]
seq=''
num=0
for i in file:
    if '>' in i:
        unknown=0
    if re.search(r'>.+unknown function',i):
        unknown=1
        list2.append(seq)
        seq=''
    else:
        if unknown==1:
            seq+=i
        if unknown==0:
            list2.append(seq)
            seq=''
if unknown==1:
    list2.append(seq)
while '' in list2:
    list2.remove('')
for item in list2:
    z=re.sub(r'\n','',item)
    list3.append(z)
print(list2)
print(len(list2))



