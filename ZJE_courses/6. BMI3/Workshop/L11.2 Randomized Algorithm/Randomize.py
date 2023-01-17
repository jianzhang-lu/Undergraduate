import random

import pandas as pd

def GenerateProbabilities(profile: pd.DataFrame, k: int, sequence: str):
    Prs = []
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i + k]
        cur_pr = 1
        for index, base in enumerate(kmer):
            pr = profile.loc[base, index]
            cur_pr *= pr
        Prs.append(cur_pr)
    return Prs


def GetBestMotif(profile: pd.DataFrame, k: int, sequence: str):
    Prs = GenerateProbabilities(profile, k, sequence)
    max_pr = max(Prs)
    max_index = Prs.index(max_pr)
    return sequence[max_index: max_index + k]


def GetBestMotifs(profile: pd.DataFrame, k: int, DNA: list) -> list:
    result = []
    for dna in DNA:
        result.append(GetBestMotif(profile, k, dna))
    return result


def Score(profile: pd.DataFrame):
    score_list = list(profile.max(axis=0))
    return sum(score_list)


def ExtractMotifs(s: list, k: int, DNA: list) -> list:
    motifs = []
    for i in range(len(s)):
        position = s[i]
        motif = DNA[i][position:position + k]
        motifs.append(motif)
    return motifs


def GenerateProfile(motifs: list, k: int):
    base_list = ['A', 'C', 'G', 'T']
    # 首先建立起count数据框
    count = [[0] * k for base in base_list]
    # 从每个motif开始遍历, 得到count的数据框
    for motif in motifs:
        for index, base in enumerate(motif):
            count[base_list.index(base)][index] += 1
    count_df = pd.DataFrame(count, index=base_list)
    col_sum = count_df.sum()
    profile_df = count_df.div(col_sum)
    return profile_df


# 核心函数, 寻找一组最佳的motifs (也就是得分最大的一组).
# start代表随机选择的每一条序列的起始位点
def FindMotifs(DNA: list, k: int, start: list):
    # counter是计数器
    counter = 0
    # 随机初始化的motifs
    cur_motifs = ExtractMotifs(start, k, DNA)
    max_score = 0
    # 定义初始化profile, 若连续两次的profile相同则结束循环
    test_profile = pd.DataFrame()

    while True:
        cur_profile = GenerateProfile(cur_motifs, k)
        cur_score = Score(cur_profile)
        if cur_score > max_score:
            max_score = cur_score
        elif cur_score < max_score:
            print('Converge wrong!')
        # 结束条件
        if cur_profile.equals(test_profile):
            return GetBestMotifs(cur_profile, k, DNA), counter
        else:
            test_profile = cur_profile
            cur_motifs = GetBestMotifs(cur_profile, k, DNA)
            counter += 1
    return cur_motifs, counter


# Gibbs sampling approach.
def GenerateProfile_LRS(motifs: list, k: int):
    base_list = ['A', 'C', 'G', 'T']
    # 首先建立起count数据框
    count = [[1] * k for base in base_list]
    # 从每个motif开始遍历, 得到count的数据框
    for motif in motifs:
        for index, base in enumerate(motif):
            count[base_list.index(base)][index] += 1
    count_df = pd.DataFrame(count, index=base_list)
    col_sum = count_df.sum()
    profile_df = count_df.div(col_sum)
    return profile_df


def Gibbs_Sampling(DNA: list, k: int, start: list):
    # counter是计数器
    counter = 0
    # 随机初始化的motifs
    cur_motifs = ExtractMotifs(start, k, DNA)
    max_score = Score(GenerateProfile_LRS(cur_motifs, k))
    # 定义初始化profile, 若连续两次的profile相同则结束循环
    test_profile = pd.DataFrame()
    finish = False

    while not finish:
        counter += 1
        # 随机选取要去掉DNA样本的顺序
        delete_indexes = random.sample(range(len(DNA)), len(DNA))
        # 从第一个index开始改进motif
        for delete_index in delete_indexes:
            delete_dna = DNA[delete_index]
            # delete完成后的motif和profile
            sub_motifs = cur_motifs[:delete_index] + cur_motifs[(delete_index+1):]
            sub_profile = GenerateProfile_LRS(sub_motifs, k)
            # 通过减少一个sequence的profile获得deleted sequence中最符合的motif
            motif_add = GetBestMotif(sub_profile, k, delete_dna)
            cur_motifs[delete_index] = motif_add
        # 全部循环后，计算改进的profile和score
        cur_profile = GenerateProfile_LRS(cur_motifs, k)
        cur_score = Score(cur_profile)

        if cur_score > max_score:
            max_score = cur_score
        # 结束条件
        if cur_profile.equals(test_profile):
            finish = True
        test_profile = cur_profile
    return cur_motifs, counter


DNA = ["TTACCTTAAC",
       "GATGTCTGTC",
       "ACGGCGTTAG",
       "CCCTAACGAG",
       "CGTCAGAGGT"]
s = [0] * len(DNA)

DNA2 = ["ATAGCTGGTCCCTAATTCCGTTCCCTGTGACCAATAGATACAACTGTCAAACCTTGACCAATAGAACAGAAGCGAAT",
        "CTGACATTGTCGAATCGAGGGAGTGTATGACCAATAGCTCGACTCGATACGTGGTAAACCCTATTGACCAATAGGTT",
        "CCGGCAACCTACCGTACGTTCTATGACCAATAGCGTGCCGAACTTATGTTAATCTGACCAATAGCACCAGCATACCC",
        "TGAGACCTCTGTCTCCTTACATGTGACCAATAGTAGGCACGCCGCTTTATCGCTTGACCAATAGAGCTTAGCTATTA",
        "ATACAATGGTTTAACAGCGATCATGACCAATAGTCCAGGTTTTGAGAGCCTAGCCTGACCAATAGCAATCATTGGCT",
        "ACCATTTGTCAATTTTATGACTGACCAATAGCTTTGCATGGCTGTAAACCGGATGCGTGACCAATAGAGCACCATCT",
        "AGCAGCCGTCGGTACCTCTAACTGACCAATAGATCCCTCGAGCTATTACCGTCCACCATGACCAATAGTCGGCCTTT",
        "ATTGCCTAGGAGACTACTTGTGTATGACCAATAGACGTAGGCCGTACACTAACTGACCAATAGAGTTCCGTCTGGCT",
        "GAAGGACCGAAGAGGGGTTTGACCAATAGCGACTTCGTAGGAGCGTGGAATTGACCAATAGTTGTATTGAGCTACGG",
        "CCGGTTAAGCAATGGGACACGTGACCAATAGTTGGCGGACACGCACGCCGGCGGTCCCAAGTGACCAATAGCGCGCA",
        "GAGGAGCACCTATAGCATGACCAATAGTGTTGCATGGACTGTGTCAATTTGAGCCGGATGATGACCAATAGTTCGCT",
        "TGACACGCAGTCCCTTAAGAGTGACCAATAGAGTCCGACGGGACGCTGAATTATGACCAATAGTACATACCCCGCAC",
        "AATTCGCACTAGAATTATCGTGACCAATAGTGGCCGGTATATTAATGAAGCGAATCTATGACCAATAGCATTAGGTA",
        "CGGCGTAGTAGGCGACAGGTGACCAATAGCGCCGGGTTCTACGTAGCGTAGAAACAGACTGTGACCAATAGCTCCTT",
        "GCTAAGTCTTCAGAGACCACATATGACCAATAGCTTCATTTGGGCCAACAACTCGATTGATGACCAATAGATAGACA",
        "CAGGGGGCTATGCTTACCCTGACCAATAGGTATCCCTAAATAGCCTCTGGCCGAATTATGACCAATAGGGGCGCGGT",
        "CTGTGAACAGACCAGAGGTAGTGACCAATAGTTCAGGCGCTACGAGCGATCAGAGGTCCTGACCAATAGATAGGCGT",
        "TGTTATTTGCTTTGTGTCTGACCAATAGTCTTGGTGGTGGACTATACCGTTGCCTATGTGACCAATAGGAGCATAAC",
        "CACCGAAGCAACGGGCCTTTCTGAACAATAGGCACAAAACCTCAAATCGACAGTAAGGTTGACCAATAGATCGAAGA",
        "GGTAAAAGGCGTTTCGGGATGACCAATAGCGGGAAATGAGGAATTGCCAGTCTGGATATGACCAATAGACGCCTGTC",
        "TGTCGTAAAGCGAGGTGGCCTGACCAATAGACAAACGCGGCGTTATGGTGATTCATTATGACCCATAGCAGTACCGA",
        "ACATGAGAATTGCTCAAAAATTGTATGACCAATAGTTCCGTCCCTAGGAGGACGAGGCATGACCAATAGATTACGAG",
        "AAAACAGAACGCGCGTTACTTTGACCAATAGTTTTCTCCAAAACACACACGTTGATTGACCAATAGTAGCAGAAATC",
        "TGCGATTGATACCTGACCAATAGTTCGAGGCTATTGGATGAAAGCAGACAGGTAGTGACCAATAGGGCTTGTCTGAC",
        "AACTTAGGCGAAGATGACAGCTATTGACCAATAGTGTCGCAGTCGGCATGCCGCTTTTCATGACCAATACATAAATT"]
s2 = [0] * len(DNA2)
# test 1 -- Converges
print(FindMotifs(DNA, 4, s))

# test 2 -- Gibbs sampling
res = Gibbs_Sampling(DNA2, 10, s2)[0]
res_dict = {}
for i in res:
    if i in res_dict:
        res_dict[i] += 1
    else:
        res_dict[i] = 1

print(res_dict)
final_res = set()
for i in res:
    if res_dict[i] == max(list(res_dict.values())):
        final_res.add(i)
print(final_res)

