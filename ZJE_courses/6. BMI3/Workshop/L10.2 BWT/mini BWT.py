def BWT_Encode(text: str):
    # 添加初始的BWT matrix
    cur_str = text
    Last = ''
    len_text = len(text)
    rotate_list = {0: text}

    for i in range(len_text-1):
        cur_str = cur_str[1:] + cur_str[0]
        rotate_list[i+1] = cur_str

    # Sort后的matrix
    sorted_list = sorted(rotate_list.items(), key=lambda s: s[1])
    SA = [i[0] for i in sorted_list]
    for each_str in sorted_list:
        Last = Last + each_str[1][-1]
    return [Last, SA]


print(BWT_Encode('acaacg$'))


# 给出某一个字符在last中的位置，返回其在first中对应的位置
def LastFirst(Last: str, cur_pos: int):
    First = ''.join(sorted(Last))
    cur_last = Last[cur_pos]
    pos = 0
    for i in First:
        if i != cur_last:
            pos += 1
        else:
            break
    number = 0
    for i in range(cur_pos):
        if Last[i] == cur_last:
            number += 1
    return number+pos


print(LastFirst('gc$aaac', 0))


def BWT_Decode(Last: str):
    # '$'一定是First的第一个, 所以原字符串的最后一位必定是Last的第一个
    cur = Last[0]
    cur_pos = 0
    res = [Last[0]]
    while cur != '$':
        cur_pos = LastFirst(Last, cur_pos)
        cur = Last[cur_pos]
        res.insert(0, cur)
    return ''.join(res[1:])


print(BWT_Decode('gc$aaac'))


def BWT_Search(text: str, pattern: str) -> list:
    res = []
    Last, SA = BWT_Encode(text)[0], BWT_Encode(text)[1]
    First = ''.join(sorted(Last))
    first_search = pattern[-1]
    candidates = []
    for index, j in enumerate(First):
        if j == first_search:
            candidates.append(index)

    while len(candidates) != 0:
        cur_pattern = [first_search]

        while True:
            cur_pos = candidates.pop()
            if ''.join(cur_pattern) == pattern:
                res.append(SA[cur_pos])
                break
            else:
                cur_pos = LastFirst(Last, cur_pos)
                if First[cur_pos] == '$':
                    break
                else:
                    candidates.append(cur_pos)
                    cur_pattern.insert(0, First[cur_pos])
    return sorted(res)


print(BWT_Search('acaacsdadfasdfdfsagsg$', 'asd'))