int_list = list(map(int, input().split(', ')))
def H_Index(alist: list, start: int, end: int):
    mid_index = (start + end)//2
    mid = alist[mid_index]
    if mid == len(alist)-mid_index:
        return mid
    if mid > len(alist)-mid_index:
        return H_Index(alist, 0, mid_index-1)
    if mid < len(alist)-mid_index:
        return H_Index(alist, mid_index+1, end)


print(H_Index(int_list, 0, len(int_list)))