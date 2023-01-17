base_dict = {'A': 'T',
             'T': 'A',
             'G': 'C',
             'C': 'G'}

def Complement(DNA: str) -> str:
    result = []
    for i in DNA:
        result.append(base_dict[i])
    return ''.join(result)
