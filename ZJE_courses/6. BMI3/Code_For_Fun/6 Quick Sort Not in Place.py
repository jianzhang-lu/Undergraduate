def QuickSort1(alist):
    if len(alist) <= 1:
        return alist[:]
    pivot = alist[0]
    left, right = [], []
    for i in alist[1:]:
        if i < pivot:
            left.append(i)
        else:
            right.append(i)
    return QuickSort1(left) + [pivot] + QuickSort1(right)