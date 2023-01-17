# 1. Score Motif
import pandas as pd
def HammingDistance(s1: str, s2: str) -> int:
    assert (len(s1) == len(s2))
    hamming_distance = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            hamming_distance += 1
    return hamming_distance


def CountMotif(DNA: list):
    base_list = ['A', 'C', 'G', 'T']
    count_res = [[0]*len(DNA[0]) for _ in range(4)]
    for dna in DNA:
        for i, j in enumerate(dna):
            count_res[base_list.index(j)][i] += 1
    return count_res


def ProfileMotif(DNA: list):
    counts = CountMotif(DNA)
    count_frame = pd.DataFrame(counts)
    dna_sum = count_frame.sum(axis=0)
    profile_frame = count_frame.div(dna_sum)
    return profile_frame


def ConsensusMotif(DNA: list):
    base_list = ['A', 'C', 'G', 'T']
    profile = ProfileMotif(DNA)
    consensus_index = profile.idxmax(axis=0).tolist()
    consensus_motif = []
    for i in consensus_index:
        consensus_motif.append(base_list[i])
    return ''.join(consensus_motif)


def ScoreMotif(DNA: list):
    consensus = ConsensusMotif(DNA)
    score = 0
    for i in DNA:
        score += HammingDistance(consensus, i)
    return score


# x, y = list(map(int, input().split(", ")))
# DNA = []
# for i in range(y):
#     DNA.append(input().split(" "))

# res = ProfileMotif(DNA)
# for row in range(4):
#     string = ''
#     for col in range(res.shape[1]):
#         string += str(res.iloc[row, col]) + ' '
#     print(string.strip())

# print(ConsensusMotif(DNA))
# print(ScoreMotif(DNA))

# 2. Median String
def NumberToSymbol(num: int) -> str:
    n_to_s = ['A', 'C', 'G', 'T']
    return n_to_s[num]


def NumberToPattern(index: int, k: int) -> str:
    if k == 1:
        return NumberToSymbol(index)
    quotient = index // 4
    remainder = index % 4
    front = NumberToPattern(quotient, k - 1)
    behind = NumberToSymbol(remainder)
    return front + behind


def SymbolToNumber(symbol: str) -> int:
    s_to_n = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    return s_to_n[symbol]


def PatternToNumber(pattern: str) -> int:
    if len(pattern) == 0:
        return 0
    else:
        length = len(pattern)
        return 4 * PatternToNumber(pattern[0:length - 1]) + SymbolToNumber(pattern[length - 1])


def generateKmer(DNA: str, k: int) -> list:
    kmers = []
    for i in range(len(DNA) - k + 1):
        kmers.append(DNA[i:i + k])
    return kmers


def MinimalDistance(pattern: str, DNA: list) -> int:
    res = 0
    for i in range(len(DNA)):
        min_dis = float('inf')
        kmers = generateKmer(DNA[i], len(pattern))
        for kmer in kmers:
            cur_dis = HammingDistance(kmer, pattern)
            if cur_dis < min_dis:
                min_dis = cur_dis
        res += min_dis
    return res


def MedianString(DNA: list, k: int):
    distances = []
    for i in range(4**k):
        pattern = NumberToPattern(i, k)
        cur_dis = MinimalDistance(pattern, DNA)
        distances.append(cur_dis)
    res = []
    for i in range(len(distances)):
        if distances[i] == min(distances):
            res.append(NumberToPattern(i, k))
    return sorted(res)


# 3. Profile Most Probable
def MostProbable(text: str, k: int, profile: list) -> str:
    n_list = ['A', 'C', 'G', 'T']
    max_prob = float('-inf')
    probable_kmer = ''
    kmers = generateKmer(text, k)
    for kmer in kmers:
        prob = 1
        for i, n in enumerate(kmer):
            prob *= profile[n_list.index(n)][i]
        if prob > max_prob:
            max_prob = prob
            probable_kmer = kmer
    return probable_kmer


