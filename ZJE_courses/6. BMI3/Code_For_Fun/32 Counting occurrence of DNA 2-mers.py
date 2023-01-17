text = input()
def PatternCount(pattern, text):
    count = 0
    for i in range(len(text)):
        if text[i:i+len(pattern)] == pattern:
            count += 1
    return count

def Count2mers(text) -> dict:
    res = {}
    for i in range(len(text)-1):
        pattern = text[i:i+2]
        res[pattern] = PatternCount(pattern, text)
    return res


res = Count2mers(text)
print(res)
n_list = ['A', 'G', 'C', 'T']
def Generate2mer(num):
    if num == 1:
        return n_list
    else:
        res = []
        fronts = Generate2mer(num-1)
        for front in fronts:
            for i in n_list:
                res.append(front+i)
        return res


final_res = {}
two_mers = Generate2mer(2)
print(two_mers)
for two_mer in two_mers:
    if two_mer in res:
        final_res[two_mer] = res[two_mer]
print(final_res)


