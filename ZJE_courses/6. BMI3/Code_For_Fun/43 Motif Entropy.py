import pandas as pd
import math
def Profile(motifs: list) -> pd.DataFrame:
    base_list = ['A', 'C', 'G', 'T']
    k_len = len(motifs[0])
    count_result = [[0] * k_len for _ in range(4)]
    for motif in motifs:
        for i, n in enumerate(motif):
            count_result[base_list.index(n)][i] += 1
    count_frame = pd.DataFrame(count_result)
    dna_sum = count_frame.sum(axis=0)
    profile_result = count_frame.div(dna_sum)
    profile_result.index = base_list
    return profile_result


def MotifEntropy(DNA: list) -> list:
    entropy_list = []
    profile = Profile(DNA)
    for index in range(len(DNA[0])):
        one_entropy = 0
        for base in range(4):
            pi = profile.iloc[base, index]
            if pi == 0:
                one_entropy -= 0
            else:
                one_entropy -= pi * math.log2(pi)
        entropy_list.append(one_entropy)
    return entropy_list



