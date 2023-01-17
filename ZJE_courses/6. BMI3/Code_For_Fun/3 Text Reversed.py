import re
def TextReverse(text: str):
    text1 = text.strip()
    pattern = re.compile(r'[^\s|a-zA-Z0-9]+')
    text2 = re.sub(pattern, '', text1)
    text_list = text2.split(' ')
    return ' '.join(reversed(text_list))

