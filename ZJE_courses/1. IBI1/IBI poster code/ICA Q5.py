# Task 5: Additional Function - Use class to get protein from DNA
RnaToProtein = {'UUU':'F','UUC':'F','UUA':'L','UUG':'L',
				'UCU':'S','UCC':'S','UCA':'S','UCG':'S',
				'UAU':'Y','UAC':'Y','UAA':'O','UAG':'U',
				'UGU':'C','UGC':'C','UGA':'X','UGG':'W',
				'CUU':'L','CUC':'L','CUA':'L','CUG':'L',
				'CCU':'P','CCC':'P','CCA':'P','CCG':'P',
				'CAU':'H','CAC':'H','CAA':'Q','CAG':'Z',
				'CGU':'R','CGC':'R','CGA':'R','CGG':'R',
				'AUU':'I','AUC':'I','AUA':'J','AUG':'M',
				'ACU':'U','ACC':'U','ACA':'U','ACG':'U',
				'AAU':'N','AAC':'B','AAA':'K','AAG':'K',
				'AGU':'S','AGC':'S','AGA':'R','AGG':'R',
				'GUU':'V','GUC':'V','GUA':'V','GUG':'V',
				'GCU':'A','GCC':'A','GCA':'A','GCG':'A',
				'GAU':'D','GAC':'D','GAA':'E','GAG':'E',
				'GGU':'G','GGC':'G','GGA':'G','GGG':'G'}

Trans = {'A':'U' , 'G':'C' , 'C':'G' , 'T':'A'}

amino_acid_mass={'A':89, 'R':174, 'N':132, 'D':133,
				 'C':121, 'E':147, 'Q':146, 'G':75,
				 'H':155, 'I':131, 'L':131, 'K':146,
				 'M':149, 'F':165, 'P':115, 'S':105,
				 'T':119, 'W':204, 'Y':181, 'V':117}

class Sequence:
	def __init__(self,name,sequence):
		self.name = name
		self.sequence =sequence

class DnaSequence(Sequence):
	def __init__(self,name,sequence):
		Sequence.__init__(self,name,sequence)
	def transcribe(self):
		NewRnaName = 'Transcribed from ' + self.name
		NewRnaSequence = ''
		for i in range(0,len(self.sequence)):
			NewRnaSequence += Trans[self.sequence[i]]
		return RnaSequence(NewRnaName,NewRnaSequence)

class RnaSequence(Sequence):
	def __init__(self,name,sequence):
		Sequence.__init__(self,name,sequence)
	def translate(self):
		NewPeptideName = 'Translated from ' +self.name
		peptide = []
		for n in range(0,len(self.sequence),3):
			condon = self.sequence[n:n+3]
			peptide.append(RnaToProtein[condon])
			PeptideSequence = ''.join(peptide)
		return PeptideSequence


DNA = 'CGTATGCGCAGCTAGCTAGCT'
MyDnaSequence = DnaSequence('MyDnaSequence',DNA)
print('DNA:',MyDnaSequence.sequence)

MyRnaSequence = MyDnaSequence.transcribe()
print('RNA:',MyRnaSequence.sequence)

MyProtein = MyRnaSequence.translate()
print('Protein:',MyProtein)

pre_mass=0
length=len(MyProtein)
for x in MyProtein:
	pre_mass += amino_acid_mass[x]
	mass = pre_mass-18*(length-1)
print('The mass is:', mass)



