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

def Tim_sort(arr):
    if len(arr) == 1:
        return arr[:]

    runs = []
    run_temp = [arr[0]]
    # state = 0: monotonically up; state = 1: monotonically down.
    state = -1
    for i in range(1, len(arr)):
        if arr[i] >= arr[i-1]:
            if len(run_temp) >= 2 and state == 1:
                runs.append(run_temp)
                run_temp = []
            run_temp.append(arr[i])
            state = 0
        else:
            if len(run_temp) >= 2 and state == 0:
                runs.append(run_temp)
                run_temp = []
            run_temp.insert(0, arr[i])
            state = 1
    if len(run_temp) > 0:
        runs.append(run_temp)

    #     Sort each run.
    sorted_arr = runs[0]
    for i in range(0, len(runs) - 1):
        sorted_arr = Merge(sorted_arr, runs[i + 1])
    return sorted_arr