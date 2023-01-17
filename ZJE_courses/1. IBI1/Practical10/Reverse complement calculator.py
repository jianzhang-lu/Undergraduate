def reverse_complement_calculator (x):
    sequence=[]
    reverse_complement=''
    for i in x:
        sequence.append(i)
    reverse_sequence=sequence[::-1]
    for base in reverse_sequence:
        if base=='A' or base=='a':
            reverse_complement+='T'
        if base=='T' or base=='t':
            reverse_complement+='A'
        if base=='C' or base=='c':
            reverse_complement+='G'
        if base=='G' or base=='g':
            reverse_complement+='C'
    return reverse_complement
# example:
# If the input sequence is AAaaaaTtttttCCCgggggg
# The output will be: CCCCCCGGGAAAAAATTTTTT
print(reverse_complement_calculator('AAaaaaTtttttCCCgggggg'))


given_sequence=input('The original DNA sequence is:')
print(reverse_complement_calculator(given_sequence))


