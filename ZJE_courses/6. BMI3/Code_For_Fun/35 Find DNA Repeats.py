text = input()
def PatternCount(pattern, text):
    count = 0
    for i in range(len(text)):
        if text[i:i+len(pattern)] == pattern:
            count += 1
    return count


res = []
for i in range(len(text)-9):
    pattern = text[i:i+10]
    if PatternCount(pattern, text) > 1:
        if pattern not in res:
            res.append(pattern)
print(res)