intergers = list(map(int, input().split(", ")))
length = int(input())
res = []
for i in range(len(intergers)-length+1):
    cur_window = intergers[i:i+length]
    res.append(max(cur_window))
print(res)

