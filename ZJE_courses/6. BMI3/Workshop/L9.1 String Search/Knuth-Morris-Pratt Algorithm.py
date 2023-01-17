def getNextList(s):
    n = len(s)
    nextList = [0, 0]
    j = 0
    for i in range(1, n):
        while j > 0 and s[i] != s[j]:
            j = nextList[j]
        if s[i] == s[j]:
            j += 1
        nextList.append(j)
    return nextList

def KMP(s, p):
    """
    Knuth-Morris-Pratt算法实现字符串查找
    """
    n = len(s)
    m = len(p)
    nextList = getNextList(p)
    indies = []
    j = 0
    for i in range(n):
        while s[i] != p[j] and j > 0:
            j = nextList[j]

        if s[i] == p[j]:
            j += 1
            if j == m:
                indies.append(i-m+1)
                j = nextList[j]
    return indies
