##############
# Question 1 #
##############

def count2mers(s: str) -> dict:
    """
    @arg s: a string
    @returns a dict
    Example: count2mers("GTAGTACTTCAGTAAGGCAC")
    returns {'GT': 3,
             'TA': 3,
             'AG': 3,
             'AC': 2,
             'CT': 1,
             'TT': 1,
             'TC': 1,
             'CA': 2,
             'AA': 1,
             'GG': 1,
             'GC': 1}
    """
    counts = {}
    for i in range(len(s)-1):
        kmer = s[i: i+2]
        if kmer not in counts:
            counts[kmer] = 1
        else:
            counts[kmer] += 1
    return counts


##############
# Question 2 #
##############

def Sort(alist):
    for i in range(len(alist)-1, 0, -1):
        exchange = False
        for j in range(0, i, 1):
            if alist[j] > alist[j + 1]:
                alist[j], alist[j + 1] = alist[j + 1], alist[j]
                exchange = True
        if not exchange:
            break
    return alist


def sortPrimers(primers: list) -> list:
    """
    @arg primers: a list of sequences
    @returns a sorted list of sequences
    Example: primers = [
        "GTAGTACTTCAGTAAGGCAC",
        "GGGGCGTGGGTGCTGTACAC",
        "AGTAAAACAAGCATACTCCC",
        "GACATGCGCATAGCGTAAGA",
        "TACCCGACGACACGAGCCTA",
        "ATGATCTGGATTTCACAAAC"]
    sortPrimers(primers)
        returns
          ['ATGATCTGGATTTCACAAAC',# (54°C)
          'AGTAAAACAAGCATACTCCC', # (56°C)
          'GTAGTACTTCAGTAAGGCAC', # (58°C)
          'GACATGCGCATAGCGTAAGA', # (60°C)
          'TACCCGACGACACGAGCCTA', # (64°C)
          'GGGGCGTGGGTGCTGTACAC'] # (68°C)
    """
    temperatures = []
    res = []
    for i in primers:
        temperature = 0
        for n in i:
            if n in ['G', 'C']:
                temperature += 4
            else:
                temperature += 2
        temperatures.append(temperature)
    unsort_temp = temperatures[:]
    sort_temp = Sort(temperatures)
    for i in sort_temp:
        res.append(primers[unsort_temp.index(i)])
    return res


##############
# Question 3 #
##############

def generateKmer(s: str, k: int):
    kmers = []
    for i in range(len(s)-k+1):
        kmers.append(s[i: i+k])
    return kmers


def longestPalindrome(s: str) -> str:
    """
    @arg s: a string
    @returns a string which is the longest palimdrome
    Example: longestPalindrome('ATGATCTGGATTTCACAAACAGTAAAACAAGCATACTCCC')
             returns ACAAACA
    """
    k = len(s)
    while k > 0:
        kmers = generateKmer(s, k)
        for kmer in kmers:
            if kmer == kmer[::-1]:
                return kmer
        k -= 1


##############
# Question 4 #
##############
m = [['G', 'T', 'G', 'G', 'T', 'C', 'T', 'T', 'T', 'G'],
     ['C', 'T', 'T', 'A', 'C', 'T', 'T', 'T', 'A', 'G'],
     ['C', 'A', 'A', 'C', 'C', 'G', 'G', 'A', 'T', 'T'],
     ['C', 'C', 'C', 'G', 'T', 'G', 'A', 'T', 'T', 'A'],
     ['G', 'A', 'G', 'A', 'C', 'T', 'T', 'G', 'G', 'A'],
     ['G', 'G', 'C', 'C', 'A', 'A', 'T', 'G', 'T', 'T'],
     ['G', 'C', 'T', 'T', 'G', 'A', 'A', 'T', 'T', 'A'],
     ['C', 'C', 'A', 'T', 'A', 'A', 'A', 'C', 'A', 'T'],
     ['A', 'G', 'A', 'C', 'A', 'C', 'A', 'C', 'C', 'T'],
     ['T', 'C', 'G', 'A', 'C', 'A', 'G', 'T', 'T', 'A']]


# Find all neighbors of the current position
def getNeighbors(cur_row, cur_col, n_row, n_col) -> list:
    directions = [[cur_row, cur_col-1],
                  [cur_row, cur_col+1],
                  [cur_row-1, cur_col],
                  [cur_row+1, cur_col]]
    neighbors = []
    for row, col in directions:
        if 0 <= row < n_row and 0 <= col < n_col:
            neighbors.append([row, col])
    return neighbors


# Judge whether the current string is the final string
def isFinal(m: list, path: list, s: str) -> bool:
    cur_s = ''
    for i in path:
        row, col = i
        sub_s = m[row][col]
        cur_s += sub_s
    return cur_s == s


# 对所有第一个位置符合的点 作为start 进行DFS
# Path记录了当前走过的路径 count记录有多少路径是符合条件的
def dfs(m: list, s: str, start: list, path: list, count: int) -> int:
    n_row = len(m)
    n_col = len(m[0])
    if isFinal(m, path, s):
        count += 1
        return count

    for neighbor in getNeighbors(start[0], start[1], n_row, n_col):
        if neighbor not in path and m[neighbor[0]][neighbor[1]] == s[len(path)]:
            path.append(neighbor)
            count = dfs(m, s, neighbor, path, count)
            path.pop()
    return count


def findSeqOccurance(m: list, s: str) -> int:
    """
    @arg m: a matrix containing nucleotide characters
    @arg s: the sequence to be searched
    Exapmle:
        findSeqOccurance(m, "GTTCCA") # returns 7
        findSeqOccurance(m, "CATAGACA") # returns 2
        findSeqOccurance(m, "GTCAGATCA") # returns 9
    """
    count = 0
    for row in range(len(m)):
        for col in range(len(m[0])):
            if m[row][col] == s[0]:
                start = [row, col]
                count += dfs(m, s, start, [start], 0)
    return count


print(findSeqOccurance(m, "GTCAGATCA"))


