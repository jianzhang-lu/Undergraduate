# DFS Algorithm
def ValidParentheses(s):
    matchDict = {'(':')',
                 '[':']',
                 '{':'}'}
    strLen = len(s)
    stackList = []
    for i in range(strLen):
        if s[i] not in matchDict.keys() and len(stackList) == 0:
            return False
        elif s[i] in matchDict.keys():
            stackList.append(s[i])
        elif s[i] == matchDict[stackList[-1]]:
            stackList.pop()
        else:
            return False

    if len(stackList) == 0:
        return True
    else:
        return False