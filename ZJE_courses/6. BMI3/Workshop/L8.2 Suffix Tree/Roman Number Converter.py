Roman = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}
string = 'MDCCXXXV'

def RomanConvert(string):
    counter = 0
    for i in range(len(string)-1):
        cur_roman, next_roman = string[i], string[i+1]
        cur_value, next_value = Roman[cur_roman], Roman[next_roman]
        if next_value > cur_value:
            counter -= cur_value
        else:
            counter += cur_value
    counter += Roman[string[-1]]
    return counter


print(RomanConvert(string))