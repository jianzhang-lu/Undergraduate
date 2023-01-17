# Task 1: Exon Counter
# Task 4: Exon Length Calculator
# The first example of question 1 and 4:
#ATTTTCTACTCCGTATCTTCCCAGCCATTGTAATTAGTTCTACCC
#
# The second example of question 1 and 4 (just for easy see):
#CCCCCCGTCCCCCAGCCCCCGTCCCCCAGCCCCGTCCCCAGCCC


sequence=input('The DNA sequence is:')
def exon_calc(seq):
	#get the introns
	x=[] # a list for the begin position of all introns
	y=[] # a list for the end position of all introns
	be=0 # the begin position of the specific intron
	tot=0 # the number of all introns
	exon_each=[] # the sequences of all exons
	exon_len=0  # the length of all exons
	tot_len=len(seq) # the length of the input sequence
	while (be<=tot_len):
		if (seq[be:be+2]=='GT'):
			x.append(be)
			p=False
			for en in range(be+2,tot_len): # the begin position of the specific intron
				if (seq[en:en+2]=='AG'):
					y.append(en+1)
					tot+=1
					be=en+2
					p=True
					break
			if(p==False):
				y.append(tot_len-1)
				tot+=1
				break
		else:
			be+=1


	#get the exons
	#specific situation: whether there is an exon in the beginning
	front=0
	if(x[0]>0):
		front=1
		new_exon=seq[0:x[0]]
		exon_each.append(new_exon)
		exon_len+=(x[0]-1)-(0)+1
	#extract exons
	for i in range(1,tot):
		new_exon=seq[y[i-1]+1:x[i]]
		exon_each.append(new_exon)
		exon_len+=(x[i]-1)-(y[i-1]+1)+1
	#specific situation: whether there is an exon in the end
	if(y[tot-1]!=tot_len-1):
		new_exon=seq[y[tot-1]+1:tot_len]
		exon_each.append(new_exon)
		exon_len+=(tot_len-1)-(y[tot-1]+1)+1
	#results
	print(sequence)
	print('Each exon:',exon_each,'\n')
	print('Number of exons:',tot+front)
	print('Length of exons:',exon_len)
	print('Percentage of exons:', exon_len/tot_len*100,end='')
	print('%')

exon_calc(sequence)
