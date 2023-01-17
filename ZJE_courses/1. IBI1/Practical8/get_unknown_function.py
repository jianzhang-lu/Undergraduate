import re
file1=open('Saccharomyces_cerevisiae.R64-1-1.cdna.all.fa','r')
file2=open("unknown_function.fa","w")
file_read=file1.read()
x=re.split('>',file_read)
for i in x:
    if 'unknown function' in i:
        a=re.findall(r'gene:(.+?)\s',i)
        new_item=re.sub(r'.+]','',i)
        b=re.sub(r'\n','',new_item)
        c=len(b)
        for e in a:
            file2.write(f'{e:14}{c}')
            file2.write(new_item)
file1.close()
file2.close()



























