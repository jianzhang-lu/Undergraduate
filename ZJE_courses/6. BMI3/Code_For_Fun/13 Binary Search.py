def BinarySearch(alist: list, target: int, start, end):
    if start > end:
        return -1
    mid_index = (start+end)//2
    mid = alist[mid_index]
    if target == mid:
        return mid_index
    elif target > mid:
        return BinarySearch(alist, target, mid_index+1, end)
    else:
        return BinarySearch(alist, target, 0, mid_index-1)


integers = list(map(int, input().split(", ")))
target = int(input())
print(BinarySearch(integers, target, 0, len(integers)-1))




