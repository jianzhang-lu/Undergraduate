integers = list(map(int, input().split(", ")))
for i in range(1, len(integers)):
    if integers[i] > integers[i-1] and integers[i] > integers[i+1]:
        print(i)
        break