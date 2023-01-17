def MotifFinder(string, n):
    kmers_dict = {}
    for i in range(len(string)-n+1):
        cur_mer = string[i:i+n]
        if cur_mer not in kmers_dict:
            kmers_dict[cur_mer] = 1
        else:
            kmers_dict[cur_mer] += 1
    res = []
    for i in kmers_dict:
        if kmers_dict[i] > 1:
            res.append(i)
    return sorted(res)


print(MotifFinder('AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT', 10))