def BubbleSort(alist):
    for i in range(len(alist)-1, 0, -1):
        exchange = False
        for j in range(0, i, 1):
            if alist[j] > alist[j + 1]:
                alist[j], alist[j + 1] = alist[j + 1], alist[j]
                exchange = True
        if not exchange:
            break
    return alist