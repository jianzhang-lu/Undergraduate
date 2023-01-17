### In place Method 1 ###
def partition2(alist, low, high):
    pivot = alist[high]
    pos = low-1
    for j in range(low, high):
        if alist[j] < pivot:
            pos += 1
            alist[pos], alist[j] = alist[j], alist[pos]

    alist[pos+1], alist[high] = alist[high], alist[pos+1]
    return pos+1


def QuickSortHelper2(alist, low, high):
    if low < high:
        pivot_index = partition2(alist, low, high)
        QuickSortHelper2(alist, low, pivot_index-1)
        QuickSortHelper2(alist, pivot_index+1, high)
    return alist


def QuickSort2(alist):
    return QuickSortHelper2(alist, 0, len(alist)-1)


print(QuickSort2([-22, -6, -7, 80, 62, 79, 14, 21]))

### In place Method 2 ###
def partition3(alist, low, high):
    pivot = alist[high]
    leftmark = low
    rightmark = high

    while leftmark < rightmark:
        while leftmark < rightmark and alist[leftmark] < pivot:
            leftmark += 1
        alist[rightmark], alist[leftmark] = alist[leftmark], alist[rightmark]

        while leftmark < rightmark and alist[rightmark] >= pivot:
            rightmark -= 1
        alist[leftmark], alist[rightmark] = alist[rightmark], alist[leftmark]

    return leftmark
def QuickSort3(alist, low, high):
    if len(alist) <= 1 or low >= high:
        return alist
    if low < high:
        pivot_index = partition3(alist, low, high)
        QuickSort3(alist, low, pivot_index - 1)
        QuickSort3(alist, pivot_index + 1, high)
    return alist

