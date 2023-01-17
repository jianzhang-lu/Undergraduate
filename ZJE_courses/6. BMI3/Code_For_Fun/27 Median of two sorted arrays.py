import json


def Median(alist):
    if len(alist) % 2 != 0:
        return alist[len(alist)//2]
    else:
        return (alist[len(alist)//2] + alist[len(alist)//2-1])/2


l = input()
list = json.loads(l)
final_list = sorted(list[0] + list[1])
median = Median(final_list)
print(format(median, '.3f'))
