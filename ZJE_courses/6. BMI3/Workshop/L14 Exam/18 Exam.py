import itertools
# # Q 1.1 Identify CHH sites
# def DNA_complement(sequence: str) -> str:
#     complement_seq = []
#     n_dict = {'A': 'T',
#               'T': 'A',
#               'G': 'C',
#               'C': 'G'}
#     for i in sequence:
#         complement_seq.append(n_dict[i])
#     return ''.join(complement_seq)
#
#
# def findCHH(S: str):
#     sites = []
#     H = ['A', 'C', 'T']
#     for i in range(len(S)-2):
#         codon = S[i: i+3]
#         if codon[0] == 'C' and codon[1] in H and codon[2] in H:
#             sites.append((i+1, codon, '+'))
#
#     # Find the back strand information
#     back = DNA_complement(S)
#     for i in range(len(back)-2):
#         codon = back[i: i+3]
#         if codon[0] in H and codon[1] in H and codon[2] == 'C':
#             sites.append((i+1, DNA_complement(codon), '-'))
#
#     res = sorted(sites, key=lambda s: s[0])
#     return res
#
#
# S = 'TATCGGAGACGAGCTAGCGAGAGC'
# print(findCHH(S))
#
# # Q 1.2 Sort word in lexicographic order
# def InsertSort(alist):
#     for i in range(1, len(alist)):
#         current_value = alist[i]
#         position = i
#         while position > 0 and current_value < alist[position-1]:
#             alist[position] = alist[position-1]
#             position -= 1
#         alist[position] = current_value
#     return alist
#
#
# length = input()
# DNA = []
# while 1:
#     dna = input()
#     if dna == '':
#         break
#     DNA.append(dna)
#
#
# print(InsertSort(DNA))


# # Q 2.1 Pancake Sorting
# def pancake_sort(numbers: list):
#     sequences = []
#     # While there are still numbers to sort
#     while numbers:
#         # Find the maximum number
#         max_num = max(numbers)
#         # Find the index of the maximum number
#         max_index = numbers.index(max_num)
#         sequences.append(max_index+1)
#         # Flip the list up to the maximum number
#         numbers = numbers[:max_index+1][::-1] + numbers[max_index+1:]
#         # Flip the entire list
#         numbers = numbers[::-1]
#         sequences.append(len(numbers))
#         # Remove the maximum number from the list
#         # 最大的数此时一定在最右侧
#         numbers.pop()
#
#     return sequences
#
#
# number = [3, 5, 2, 4, 1]
# print(pancake_sort(number))


# Q 3.1 Longest common substring
#
# def longest_common_substring(stringX, stringY):
#     # Initialize the lengths of the strings
#     m = len(stringX)
#     n = len(stringY)
#     # Initialize the longest common substring length to 0
#     longest_length = 0
#     # Initialize the longest common substring to an empty string
#     longest_substring = ""
#     # Create a two-dimensional list to store the lengths of common substrings
#     lengths = [[0 for _ in range(n+1)] for __ in range(m+1)]
#
#     # Iterate over the characters in both strings
#     for i in range(1, m+1):
#         for j in range(1, n+1):
#             # If the characters are equal, add 1 to the length of the common substring
#             if stringX[i-1] == stringY[j-1]:
#                 lengths[i][j] = lengths[i-1][j-1] + 1
#
#                 # Update the longest common substring if necessary
#                 if lengths[i][j] > longest_length:
#                     longest_length = lengths[i][j]
#                     longest_substring = stringX[i-longest_length:i]
#             # If the characters are not equal, the length of the common substring is 0
#             else:
#                 lengths[i][j] = 0
#
#     # Return the longest common substring and its length
#     return longest_length, longest_substring
#
#
# print(longest_common_substring('ATCGGTGACG', 'TATCGATCGGC'))


# Q 3.2 Best Time to Buy and Sell Stock
# def Max_profit(prices):
#     # Initialize the minimum price seen so far and the maximum profit to 0
#     min_price = float('inf')
#     max_profit = 0
#
#     # Iterate over the prices
#     for price in prices:
#         # Update the minimum price seen so far
#         min_price = min(min_price, price)
#
#         # Update the maximum profit
#         max_profit = max(max_profit, price - min_price)
#
#     # Return the maximum profit
#     return max_profit
#
#
# test1 = [7, 1, 5, 3, 6, 4]
# print(Max_profit(test1))
#
# test2 = [7, 6, 4, 3, 1]
# print(Max_profit(test2))


# Q 4.1 Scooting during COVID-19
# def Find_shortest_route(times):
#     # Initialize the shortest route and total time to infinity
#     shortest_route = float('inf')
#     shortest_time = float('inf')
#
#     # Iterate over all possible routes
#     for route in itertools.permutations(range(2, 8)):
#         # Calculate the total time for the current route
#         total_time = times[0][route[0]-1]
#         for i in range(len(route)-1):
#             total_time += times[route[i]-1][route[i+1]-1]
#         total_time += times[route[-1]-1][0]
#
#         # Update the shortest route and time if necessary
#         if total_time < shortest_time:
#             shortest_route = route
#             shortest_time = total_time
#
#     # Return the shortest route and total time
#     return shortest_route, shortest_time
#
#
# matrix = [[0, 38, 22, 27, 15, 18, 16],
#           [40, 0, 42, 47, 52, 47, 45],
#           [16, 37, 0, 7, 19, 28, 13],
#           [23, 46, 9, 0, 15, 25, 6],
#           [15, 51, 22, 18, 0, 9, 11],
#           [22, 44, 32, 31, 11, 0, 18],
#           [14, 43, 15, 8, 9, 15, 0]]
# print(Find_shortest_route(matrix))

