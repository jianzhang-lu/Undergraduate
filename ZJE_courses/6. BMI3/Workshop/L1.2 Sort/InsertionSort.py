def InsertSort(alist):
    for i in range(1, len(alist)):
        current_value = alist[i]
        position = i
        while position > 0 and current_value < alist[position-1]:
            alist[position] = alist[position-1]
            position -= 1
        alist[position] = current_value
    return alist