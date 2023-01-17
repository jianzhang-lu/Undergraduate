# Find motif by Greedy Algorithm
import pandas as pd

def generateKmer(DNA: str, k: int):
    kmers = []
    for i in range(len(DNA) - k + 1):
        kmers.append(DNA[i:i + k])
    return kmers


def Profile(motifs: list) -> pd.DataFrame:
    base_list = ['A', 'C', 'G', 'T']
    k_len = len(motifs[0])
    count_result = [[1] * k_len for _ in range(4)]
    for motif in motifs:
        for i, n in enumerate(motif):
            count_result[base_list.index(n)][i] += 1
    count_frame = pd.DataFrame(count_result)
    dna_sum = count_frame.sum(axis=0)
    profile_result = count_frame.div(dna_sum)
    profile_result.index = base_list
    return profile_result


def ProfileMostProbable(motif_profile: pd.DataFrame, k: int, DNA: str):
    most_probability = float('-inf')
    kmer_result = ''
    kmers = generateKmer(DNA, k)
    for kmer in kmers:
        cur_probability = 1
        for i in range(k):
            pr = motif_profile.loc[kmer[i], i]
            cur_probability *= pr
        if cur_probability > most_probability:
            most_probability = cur_probability
            kmer_result = kmer
    return kmer_result


def HammingDistance(s1: str, s2: str):
    hamming_distance = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            hamming_distance += 1
    return hamming_distance


def SCORE(motifs: list):
    # 寻找consensus motif
    profile = Profile(motifs)
    consensus_motif = ''.join(list(profile.idxmax()))
    # 计算score
    score = 0
    for motif in motifs:
        score += HammingDistance(consensus_motif, motif)
    return score


def GreedyMotifSearch(DNA: list, k: int, t: int):
    best_motifs = []
    for i in DNA:
        best_motifs.append(i[0:k])
    kmers = generateKmer(DNA[0], k)
    for kmer in kmers:
        motifs = [kmer]
        for i in range(1, t):
            profile = Profile(motifs)
            best = ProfileMostProbable(profile, k, DNA[i])
            motifs.append(best)
        if SCORE(motifs) < SCORE(best_motifs):
            best_motifs = motifs
    return best_motifs


DNA = ["ATGCCGT", "CGTAGTA", "GGGGTACAC", "ACACTACG", "TATAGACT"]

print(GreedyMotifSearch(DNA, 3, 5))

# ['ATG', 'TAG', 'TAC', 'TAC', 'TAG']