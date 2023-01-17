Molecular_weights = [
    {'Aminoacid': 'Alanine', 'OneLetter': 'A', 'MolecularWeight': 71.08},
    {'Aminoacid': 'Cysteine', 'OneLetter': 'C', 'MolecularWeight': 103.12},
    {'Aminoacid': 'Aspartic acid', 'OneLetter': 'D', 'MolecularWeight': 115.09},
    {'Aminoacid': 'Glutamic acid', 'OneLetter': 'E', 'MolecularWeight': 129.11},
    {'Aminoacid': 'Phenylalanine', 'OneLetter': 'F', 'MolecularWeight': 147.17},
    {'Aminoacid': 'Glycine', 'OneLetter': 'G', 'MolecularWeight': 57.05},
    {'Aminoacid': 'Histidine', 'OneLetter': 'H', 'MolecularWeight': 137.14},
    {'Aminoacid': 'Lysine', 'OneLetter': 'K', 'MolecularWeight': 128.17},
    {'Aminoacid': 'Leucine', 'OneLetter': 'L', 'MolecularWeight': 113.16},
    {'Aminoacid': 'Methionine', 'OneLetter': 'M', 'MolecularWeight': 131.20},
    {'Aminoacid': 'Asparagine', 'OneLetter': 'N', 'MolecularWeight': 114.10},
    {'Aminoacid': 'Proline', 'OneLetter': 'P', 'MolecularWeight': 97.12},
    {'Aminoacid': 'Glutamine', 'OneLetter': 'Q', 'MolecularWeight': 128.13},
    {'Aminoacid': 'Arginine', 'OneLetter': 'R', 'MolecularWeight': 156.19},
    {'Aminoacid': 'Serine', 'OneLetter': 'S', 'MolecularWeight': 87.08},
    {'Aminoacid': 'Threonine', 'OneLetter': 'T', 'MolecularWeight': 101.10},
    {'Aminoacid': 'Valine', 'OneLetter': 'V', 'MolecularWeight': 99.13},
    {'Aminoacid': 'Tryptophan', 'OneLetter': 'W', 'MolecularWeight': 186.21},
    {'Aminoacid': 'Tyrosine', 'OneLetter': 'Y', 'MolecularWeight': 163.17}
]

input_mass = [0, 101.1, 163.17, 238.24, 250.25, 321.33, 367.35, 438.43, 450.44, 552.53, 613.61, 639.61, 769.8, 825.82, 898.91, 954.93, 998.04, 1085.12, 1111.12, 1156.2, 1297.33, 1342.41, 1368.41, 1455.49, 1498.6, 1554.62, 1627.71, 1683.73, 1813.92, 1839.92, 1901.0, 2003.09, 2015.1, 2086.18, 2132.2, 2203.28, 2215.29, 2290.36, 2352.43, 2453.53]


def FindPeptide(alist: list, weight: float):
    for i in alist:
        if i['MolecularWeight'] == round(weight, 2):
            return alist.index(i)
    return -1


def AddGraph(graph: dict, graph_line: tuple) -> dict:
    start, end, edge = graph_line
    if start not in graph:
        graph[start] = {end: edge}
    else:
        graph[start][end] = edge
    return graph


def GenerateGraph(input_mass: list) -> dict:
    graph = {}
    for i in range(len(input_mass)):
        for j in range(i+1, len(input_mass)):
            diff = input_mass[j] - input_mass[i]
            pep_index = FindPeptide(Molecular_weights, diff)
            if pep_index != -1:
                peptide = Molecular_weights[pep_index]['OneLetter']
                # (list[i], list[j], peptide): (0, 129.11, E)
                graph_line = (input_mass[i], input_mass[j], peptide)
                graph = AddGraph(graph, graph_line)
    return graph


def PeptideIdent(graph: dict, input_mass: list, start, res, temp):
    if start == input_mass[-1]:
        res.append(temp)
        return res

    for i in graph[start]:
        cur_peptide = graph[start][i]
        temp.append(cur_peptide)
        res = PeptideIdent(graph, input_mass, i, res, temp)
        # 重点：temp应该加到这里！！！
        temp = []
    return res


graph = GenerateGraph(input_mass)
peptides = PeptideIdent(graph, input_mass, input_mass[0], [], [])
# 寻找最大长度的结果
nums = []
for i in range(len(peptides)):
    nums.append(len(peptides[i]))

for i in range(len(nums)):
    if nums[i] == max(nums):
        print(''.join(peptides[i]))