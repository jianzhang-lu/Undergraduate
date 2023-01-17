# Problem 1
## Do not consider reverse complement strand.
def GenerateKmers(DNA: str, k: int) -> list:
    kmers = []
    for i in range(len(DNA)-k+1):
        kmers.append(DNA[i:i+k])
    return kmers


def KmerFreq(DNA: str, pattern:str) -> int:
    count = 0
    kmers = GenerateKmers(DNA, len(pattern))
    for kmer in kmers:
        if kmer == pattern:
            count += 1
    return count

## Consider reverse complement strand
def DNA_reverse(sequence: str) -> str:
    return sequence[::-1]


def DNA_complement(sequence: str) -> str:
    complement_seq = []
    n_dict = {'A': 'T',
              'T': 'A',
              'G': 'C',
              'C': 'G'}
    for i in sequence:
        complement_seq.append(n_dict[i])
    return ''.join(complement_seq)


def KmerFreqBothStrand(DNA: str, pattern: str) -> dict:
    forward = DNA
    backward = DNA_reverse(DNA_complement(DNA))
    for_count = KmerFreq(forward, pattern)
    back_count = KmerFreq(backward, pattern)
    return {'forward': for_count,
            'backward': back_count}

# Problem 2
def MostFreqKmer(DNA: str, k: int) -> list:
    MostFreq = []
    kmers = GenerateKmers(DNA, k)
    count = {}
    for kmer in kmers:
        if kmer not in count:
            count[kmer] = 1
        else:
            count[kmer] += 1
    max_count = max(count.values())
    for key, value in count.items():
        if value == max_count:
            MostFreq.append(key)
    return MostFreq


# Problem 3
def miniBLAST(shortDNA: str, wholeDNA: str) -> list:
    position = []
    kmers = GenerateKmers(wholeDNA, len(shortDNA))
    for index, kmers in enumerate(kmers):
        if kmers == shortDNA:
            position.append(index)
    return position

# Problem 4
def myBLAST(shortDNA: str, wholeDNA: str) -> dict:
    forward = wholeDNA
    backward = DNA_reverse(DNA_complement(wholeDNA))
    forward_result = miniBLAST(shortDNA, forward)
    backward_result = miniBLAST(shortDNA, backward)
    position = {'forward': forward_result,
                'backward': backward_result}
    return position

# Problem 5
def HammingDistance(s1: str, s2: str) -> int:
    assert (len(s1) == len(s2))
    hamming_distance = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            hamming_distance += 1
    return hamming_distance

## 先只考虑单个方向的情况
def miniBLASTwithMismatch(shortDNA: str, wholeDNA: str, mismatch: int) -> list:
    position = []
    kmers = GenerateKmers(wholeDNA, len(shortDNA))
    for index, kmers in enumerate(kmers):
        if HammingDistance(kmers, shortDNA) <= mismatch:
            position.append(index)
    return position

## 再考虑正反双链
def myBLASTwithMismatch(shortDNA: str, wholeDNA: str, mismatch:int) -> dict:
    forward = wholeDNA
    backward = DNA_reverse(DNA_complement(wholeDNA))
    forward_result = miniBLASTwithMismatch(shortDNA, forward, mismatch)
    backward_result = miniBLASTwithMismatch(shortDNA, backward, mismatch)
    position = {'forward': forward_result,
                'backward': backward_result}
    return position


# test
shortDNA = 'ATAT'
DNA_sequence = 'GATATATGCATATACTT'
print(myBLASTwithMismatch(shortDNA, DNA_sequence, 3))