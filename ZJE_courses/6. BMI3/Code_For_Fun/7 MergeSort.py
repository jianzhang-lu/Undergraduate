def MergeSort(alist):
    if len(alist) <= 1:
        return alist[:]
    else:
        medium = len(alist)//2
        left_list = MergeSort(alist[:medium])
        right_list = MergeSort(alist[medium:])
        return Merge(left_list, right_list)
def Merge(left_list, right_list):
    result = []
    i = 0
    j = 0
    while i < len(left_list) and j < len(right_list):
        if left_list[i] < right_list[j]:
            result.append(left_list[i])
            i += 1
        else:
            result.append(right_list[j])
            j += 1
    while i < len(left_list):
        result.append(left_list[i])
        i += 1
    while j < len(right_list):
        result.append(right_list[j])
        j += 1
    return result