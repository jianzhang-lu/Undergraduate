# string: size n
# pattern: size m
# K: len([A, C, G, T])
# q: to limit memory
# 对于ATTCC:
# T(TTCC) = T(ATTC)*4 + T(C) - T(A) * constant
# constant = 4**4
def RabinKarp(string, pattern, K=4, q=10):
    res = []
    n = len(string)
    m = len(pattern)
    constant = K**m % q
    base = ['A', 'C', 'G', 'T']
    # 计算string中第一个m长度字符串的哈希值, 顺便计算pattern的哈希值
    Ts = 0
    Tp = 0
    for i in range(m):
        Ts = (base.index(string[i]) + Ts*K) % q
        Tp = (base.index(pattern[i]) + Tp*K) % q
    # 开始搜索
    for i in range(n-m+1):
        if Tp == Ts:
            if pattern == string[i:i+m]:
                res.append(i)
        else:
            # 滚动哈希值
            Ts = (Ts*K + base.index(string[i+m]) - constant*base.index(string[i])) % q
    return res


print(RabinKarp('ATTCCGTAAATTCCAAAATTCCGATTCTCC', 'TTCC'))