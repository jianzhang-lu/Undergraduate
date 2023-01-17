money = 140
pences = [1, 10, 21, 34, 70, 100]
minimal = [[x] + [0]*(len(pences)-1) for x in range(money+1)]

for i in range(1, money+1):
    for j in range(len(pences)):
        if pences[j] <= i and sum(minimal[i-pences[j]])+1 < sum(minimal[i]):
            # 以11举例, 11本身为[11, 0, 0, 0, 0, 0], 实际应该是[1, 1, 0, 0, 0, 0]
            # 等于1的[1, 0, 0, 0, 0, 0]再加上更改的第二个元素(10块)
            pre_manner = minimal[i-pences[j]][:]  # [1, 0, 0, 0, 0, 0]
            pre_manner[j] += 1  # [1, 1, 0, 0, 0, 0]
            minimal[i] = pre_manner

