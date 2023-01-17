DNA = 'ATACAGGAGATTTATAAGAGATATAAAGAGATAGCAGATA'
forward = 'TATAAA'
backward = 'TTTATA'
def FindTATA(DNA: str):
    for i in range(len(DNA)-5):
        if DNA[i:i+6] == backward:
            print(i, backward, '-')
        if DNA[i:i+6] == forward:
            print(i, forward, '+')
    return 0


FindTATA(DNA)

