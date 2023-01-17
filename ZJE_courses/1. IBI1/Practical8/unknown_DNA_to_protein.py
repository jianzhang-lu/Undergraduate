import re
file=input('The filename is:')
#file1=open('Saccharomyces_cerevisiae.R64-1-1.cdna.all.fa','r')
file1=open(file)
file2=open("protein_sequence.fa",'w')
file_read=file1.read()
x=re.split('>',file_read)
m=0
str_protein=''
translation_codons = {"TTT": "F",
                      "TTC": "F",
                      "TTA": "L",
                      "TTG": "L",
                      "CTT": "L",
                      "CTC": "L",
                      "CTA": "L",
                      "CTG": "L",
                      "ATT": "I",
                      "ATC": "I",
                      "ATA": "J",
                      "ATG": "M",
                      "GTT": "V",
                      "GTC": "V",
                      "GTA": "V",
                      "GTG": "V",
                      "TCT": "S",
                      "TCC": "S",
                      "TCA": "S",
                      "TCG": "S",
                      "CCT": "P",
                      "CCC": "P",
                      "CCA": "P",
                      "CCG": "P",
                      "ACT": "T",
                      "ACC": "T",
                      "ACA": "T",
                      "ACG": "T",
                      "GCT": "A",
                      "GCC": "A",
                      "GCA": "A",
                      "GCG": "A",
                      "TAT": "Y",
                      "TAC": "Y",
                      "TAA": "O",
                      "TAG": "U",
                      "CAT": "H",
                      "CAC": "H",
                      "CAA": "Q",
                      "CAG": "Z",
                      "AAT": "N",
                      "AAC": "B",
                      "AAA": "K",
                      "AAG": "K",
                      "GAT": "D",
                      "GAC": "D",
                      "GAA": "E",
                      "GAG": "E",
                      "TGT": "C",
                      "TGC": "C",
                      "TGA": "X",
                      "TGG": "W",
                      "CGT": "R",
                      "CGC": "R",
                      "CGA": "R",
                      "CGG": "R",
                      "AGT": "S",
                      "AGC": "S",
                      "AGA": "R",
                      "AGG": "R",
                      "GGT": "G",
                      "GGC": "G",
                      "GGA": "G",
                      "GGG": "G"}
for i in x:
    if 'unknown function' in i:
        a=re.findall(r'gene:(.+?)\s',i)
        new_item=re.sub(r'.+]','',i)
        b=re.sub(r'\n','',new_item)
        while m<len(b):
            protein=b[m:m+3]
            z=translation_codons[protein]
            str_protein+=z
            m+=3
        final_protein=str_protein
        str_protein=''
        m=0
        c=len(b)/3
        for e in a:
            file2.write(e)
            file2.write('\t\t\t')
            file2.write(str(c))
            file2.write('\n')
            file2.write(final_protein)
            file2.write('\n')
file1.close()
file2.close()

