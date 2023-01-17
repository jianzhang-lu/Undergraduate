seq='ATGCGACTACGATCGAGGGCC'
table={'ATG':'M','CGA':'R','CTA':'L', 'TCG':'S', 'AGG':'R', 'GCC':'A'}
i=0
while i<len(seq):
    code=seq[i:i+3]
    print(table[code],end="")
    i+=3









