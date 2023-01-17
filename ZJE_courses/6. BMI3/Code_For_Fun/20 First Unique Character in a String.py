string = input()
str_dict = {}
for i in string:
    print(i)
    if i not in str_dict:
        str_dict[i] = 1
    else:
        str_dict[i] += 1

have = True
for i in range(len(string)):
    if str_dict[string[i]] > 1:
        have = False
    else:
        have = True
        print(i)
        break
if not have:
    print(-1)