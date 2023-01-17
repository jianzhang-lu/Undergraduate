import numpy as np

# 计算一个list中 -出现的概率
def CalculatePro(alist) -> float:
    counter = 0
    for i in alist:
        if i == '-':
            counter += 1
    return counter/len(alist)


# 根据threshold排除掉一些不符合要求的位置
def Filter(proteins: list, threshold: float) -> np.array:
    rest_proteins = []
    rest_pos_index = []
    for pos_index in range(len(proteins[0])):
        pos_list = [i[pos_index] for i in proteins]
        if CalculatePro(pos_list) <= threshold:
            rest_pos_index.append(pos_index)

    for protein in proteins:
        rest_protein = [protein[i] for i in rest_pos_index]
        rest_proteins.append(rest_protein)
    return np.array(rest_proteins)


# 根据过滤后的proteins找到所有的peptide
# return: ["A", "C", "D", "E", "G"]
def FindPeptide(all_proteins: list, threshold: float) -> list:
    proteins = Filter(all_proteins, threshold)
    peptides = []
    for protein in proteins:
        for i in protein:
            if i not in peptides and i != '-':
                peptides.append(i)
    return sorted(peptides)


# 生成index列表(["S", "I0", "M1", "D1", "I1", "M2", "D2", "I2", "M3", "D3", "I3", "E"])
# I: insertion; D: deletion; M: match/dis-match; state的个数即为IMD的组数
def FindIndex(all_proteins: list, threshold: float) -> list:
    index = ['S', 'I0']
    proteins = Filter(all_proteins, threshold)
    states_num = len(proteins[0])
    for state in range(states_num):
        for i in ['M', 'D', 'I']:
            index.append(i + str(state+1))
    index.append('E')
    return index


def FindEmission(proteins: np.array):
    pass


def FindTransition(proteins: np.array, index: list):
    transition = np.zeros((len(index), len(index)))
    for i in range(len(proteins[0])):
        # 提出每一个
        pass



threshold = 0.252
proteins = ['EDEACADGE', 'EDDA--DA-', 'EDEAC-DA-', 'CDEA---A-', 'CD-ACG-AG']
res_proteins = Filter(proteins, threshold)
index = FindIndex(proteins, threshold)

# threshold = float(input())
# proteins = []
# while 1:
#     protein = input()
#     if protein == '':
#         break
#     proteins.append(protein)

