#!/usr/bin/env python3
# -*- coding: utf━8 -*-
# This is the template for BMI3 Coding Challenge (A)

# Technical Instructions
# Timing:
# You have 2 hours to complete this assignment. 
# How many questions:
# There are 11 questions (question section 1━6), you only need to choose 
# one out of the two for each question section 1-5 (i.e. In total, you only 
# need to answer 6 questions). If you answer more than 6 question, the staff 
# will only mark the first question of the two within the same question section. 


# Installation before the exam:
# As stated in the final exam instructions (released 2 weeks before the final), 
# you should install numpy, pandas, matplotlib, seaborn python package before the exam. 
# If you have any problem installing these packages, please contact the teaching faculties 
# or TAs as soon as possible. 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from typing import List, Optional

# What python module you can use:
# You can use any module you feel is useful unless it's specified in the question 
# that you cannot use it.

#                          SECTION 1 (15 points)
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Question 1.1: Debug the code finding overlaping sequences   ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
# sequence_1 = 'TNEKLFFGSGTQLSVL'
# sequence_2 = 'CASSGGPENEKLFF'
#
# def overlap_with_truncation(sequence_1: str, sequence_2: str):
#     for n in range(len(sequence_1)):
#         for i in range(1,n):
#             if sequence_2.endswith(sequence_1[i:n]):
#                 return sequence_1[i:n]
#
# print(overlap_with_truncation(sequence_1, sequence_2))
#
# #Explanation (less than 50 words):
#
# #Correct Code:
# def overlap_with_truncation_corrected(sequence_1: str, sequence_2: str):
#     # REMOVE THE FOLLOWING LINE AND WRITE YOUR CODE HERE
#     raise NotImplementedError()
#
# print(overlap_with_truncation_corrected(sequence_1, sequence_2))

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃   Question 1.2: Debug the code adding ones to each element    ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#  Note: You should not use the `copy` module in your correction

a = [[1, 2], [2, 3], [3, 4]]


def add_one(arr: List[List[int]]):
    ret = []
    for i in arr:
        i[0] += 1
        ret.append(i)
    return arr, ret


print(add_one(a))


# Explanation (less than 50 words):
# This code only add 1 to the first element of each subarray. That is, it returns [[2, 2], [3, 3], [4, 4]]

# Correct Code:
def add_one_corrected(arr: List[List[int]]):
    modified = []
    for i in arr:
        modified_sublist = []
        for number in i:
            modified_sublist.append(number + 1)
        modified.append(modified_sublist)
    return arr, modified


print(add_one_corrected(a))

#                          SECTION 2 (15 points)
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃               Question 2.1: Sorting genomic locations         ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

# example_input_2_1 = [
#     'chr11-9159454-9159490',
#     'chr8-37559304-37559340',
#     'chr1-28764748-28764784',
#     'chr7-142219166-142219202',
#     'chr1-205493625-205493661'
# ]
#
#
# def sort_genomic_locations(locations: List[str]):
#     # REMOVE THE FOLLOWING LINE AND WRITE YOUR CODE HERE
#     raise NotImplementedError()
#
#
# print(sort_genomic_locations(example_input_2_1))

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃             Question 2.2: Sorting amino acid sequences        ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

molecular_weights = {
    'A': 89.1,
    'R': 174.2,
    'N': 132.12,
    'D': 133.11,
    'C': 121.16,
    'E': 147.13,
    'Q': 146.15,
    'G': 75.07,
    'H': 155.16,
    'O': 131.13,
    'I': 131.18,
    'L': 131.18,
    'K': 146.19,
    'M': 149.21,
    'F': 165.19,
    'P': 115.13,
    'U': 139.11,
    'S': 105.09,
    'T': 119.12,
    'W': 204.23,
    'Y': 181.19,
    'V': 117.15
}

example_input_2_2 = [
    'FEAOHLGPQF',
    'GORPDWMDO',
    'TSICEERU',
    'AMUTATQE',
    'IWEUEGWVY',
    'NGMKKOHYDU',
    'RUNWYIRCD',
    'AVUYEYOVTM',
    'FURGIWDEF',
    'DLQPRYPAS',
]

# Implement the Merge sort
def MergeSort(alist):
    if len(alist) <= 1:
        return alist[:]
    else:
        medium = len(alist)//2
        left_list = MergeSort(alist[:medium])
        right_list = MergeSort(alist[medium:])
        return Merge(left_list, right_list)


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


def sortby_molecular_weight(sequences: List[str]):
    res = []
    weights = []
    for sequence in sequences:
        one_weight = 0
        for aa in sequence:
            one_weight += molecular_weights[aa]
        weights.append(one_weight)
    unsort_weighs = weights[:]
    sorted_weights = MergeSort(weights)
    for i in sorted_weights:
        res.append(sequences[unsort_weighs.index(i)])
    print(res)
    return res


sortby_molecular_weight(example_input_2_2)


#                          SECTION 3 (15 points)
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃      Question 3.1: Maximal number of slicing windows.         ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

example_input_3_1 = dict(
    nums=[1, 3, 0, 0, 5, 3, 6, 7],
    k=3
)


def maximal_number_of_slicing_windows(nums: List[int], k: int):
    max_numbers = []
    for i in range(len(nums)-k+1):
        max_number = float('-inf')
        num = nums[i: i+k]
        for i in num:
            if i > max_number:
                max_number = i
        max_numbers.append(max_number)
    print(max_numbers)
    return max_numbers


maximal_number_of_slicing_windows(example_input_3_1['nums'], example_input_3_1['k'])

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃               Question 3.2: Wild Card Matching                ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
# example_input_3_2 = dict(
#     s="TCATGTGATTGTAGGGGCTGTGTGGTCTGAAATCTGTGGGACAGGCCAGCAGGCTGGAAACTCAGGTAGGAGTTGATGCTGGGGGTTTTTCGTTTTGTTTGTTTAGTTTTGGTTTTGGTTTGGGGACTTTTGGAGACTGGGTCTCACTCCTGTCGCCCAGGCTAGAGTGCAGTGGGAGCAATCACAGCTCACTGCAGCCTTGACTTCCTGGGCTCAGGTGATTCTCCCACCTCAGCCTCCCGAGTAGCTGGGATTACAGGTGTGAGCCACCATGCTCGGCTATTTTTTTTTTTTGTATTTTTAGTAGAGACAGACTTTTTCCATATTGCCCAGGCTGGTCTCAAAACTTCCGAGCTCAAGCAATCTTCCCTCCTCGGCCTCCCAAAGTGCAGGGATTACAGGCATGAGCCACTGTGCCTG",
#     pattern="DCAWG"
# )
#
#
# def wild_card_matching(s: str, pattern: str):
#     # REMOVE THE FOLLOWING LINE AND WRITE YOUR CODE HERE
#     raise NotImplementedError()
#
#
# wild_card_matching(example_input_3_2['s'], example_input_3_2['pattern'])

#                          SECTION 4 (20 points)
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃      Question 4.1 Lowest common ancestors of trie tree        ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

# example_input_4_1 = dict(
#     trie=['AT', 'CG', 'AC', 'GT', 'G', 'C', None, None, 'TA', 'C', None, 'G', None, None, None, None, 'GA', 'T', None,
#           'T', None, None],
#     node_1='ATG',
#     node_2='ATC'
# )
#
#
# def lca_trie(trie: List[Optional[str]], node_1: str, node_2: str):
#     # REMOVE THE FOLLOWING LINE AND WRITE YOUR CODE HERE
#     raise NotImplementedError()
#
#
# print(lca_trie(example_input_4_1['trie'], example_input_4_1['node_1'], example_input_4_1['node_2']))

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                Question 4.2 Graph With A Cycle                ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

example_input_4_2 = [
    ('v1', 'v2'),
    ('v2', 'v3'),
    ('v3', 'v4'),
    ('v3', 'v7'),
    ('v4', 'v5'),
    ('v5', 'v6'),
    ('v7', 'v8'),
    ('v8', 'v9'),
    ('v9', 'v3')
]


def Generate_graph(graph: dict, graph_line: tuple) -> dict:
    start, end = graph_line
    if start not in graph:
        graph[start] = [end]
    else:
        graph[start].append(end)
    return graph


def graph_with_cycle(graph):
    # Generate the graph
    graph_dict = {}
    for i in graph:
        graph_dict = Generate_graph(graph_dict, i)
    # print(graph_dict)
    # Store the visited vertices
    visit, cur_visit = set(), set()
    for vertex in graph_dict:
        if vertex not in visit:
            if dfs(vertex, graph_dict, visit, cur_visit):
                return True
    return False


def dfs(vertex, graph_dict, visit, cur_visit):
    cur_visit.add(vertex)
    if vertex in graph_dict:
        for neighbor in graph_dict[vertex]:
            if neighbor not in visit:
                if dfs(neighbor, graph_dict, visit, cur_visit):
                    return True
            else:
                return True
        cur_visit.remove(vertex)
        visit.add(vertex)
    # No cycle is found
    return False


print(graph_with_cycle(example_input_4_2))

#                          SECTION 5 (25 points)
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                 Question 5.1 Finding Substring                ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

example_input_5_1 = dict(
    matrix=[
        ['A', 'C', 'C', 'G', 'T', 'C', 'T', 'T', 'A', 'T'],
        ['C', 'C', 'C', 'A', 'G', 'T', 'A', 'G', 'G', 'T'],
        ['T', 'G', 'G', 'G', 'A', 'T', 'G', 'G', 'G', 'C'],
        ['C', 'A', 'T', 'C', 'G', 'C', 'A', 'G', 'T', 'G'],
        ['C', 'C', 'T', 'T', 'T', 'T', 'C', 'T', 'G', 'C']
    ],
    substring="AGATGA")

# DFS: Test whether the rest of the substring can be found in the matrix
def check_substring(matrix, i, j, substring):
    if not substring:
        return []

    # Check the below position
    if i < len(matrix)-1 and matrix[i+1][j] == substring[0]:
        path = check_substring(matrix, i+1, j, substring[1:])
        if path is not None:
            return [(i+1, j)] + path

    # Check the right position
    if j < len(matrix[0])-1 and matrix[i][j+1] == substring[0]:
        path = check_substring(matrix, i, j+1, substring[1:])
        if path is not None:
            return [(i, j+1)] + path

    # The substring was not found
    return None


def find_substring(matrix: List[List[str]], substring: str):
    # m: row, n: col
    m = len(matrix)
    n = len(matrix[0])
    has_path = False

    for i in range(m):
        for j in range(n):
            # Test if the start position is correct
            if matrix[i][j] == substring[0]:
                path = check_substring(matrix, i, j, substring[1:])
                if path is not None:
                    has_path = True
                    # Add the start position of the path
                    path = [(i, j)] + path
                    return has_path, path

    # No Path was found
    return has_path


print(find_substring(example_input_5_1['matrix'], example_input_5_1['substring']))

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃           Question 5.2 Building De Bruijin Graph              ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
# example_input_5_2 = [
#     'CTGTGCAACCGATGTGCTTA',
#     'AAGCGTCCCCAGCCTGTATT'
# ]
#
#
# def build_de_bruijin_graph(sequences: List[str]):
#     # REMOVE THE FOLLOWING LINE AND WRITE YOUR CODE HERE
#     raise NotImplementedError()
#
#
# print(build_de_bruijin_graph(example_input_5_2))

#                          SECTION 6 (10 points)
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                 Question 6 Short Answer Question              ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

# Use specific example to illustrate how bioinformatics algorithms could be used 
# to solve real-life biomedical problem. Note: you cannot use your ICA mini-project 
# as example (10points) [no more than 150 words]

# Answer:
# One specific example of the application of bioinformatics algorithms in biomedical problems is the analysis of genetic mutations in some diseases.
# To be specific, if a patient has a genetic disease and had done the RNA-seq. We can use BWT algorithms to analyze the patient’s sequence
# and align it to the reference genome, which could help us identify the mutations.
# Another example: In tumors, in order to study the tumor microenvironment, single-cell RNA-seq is an excellent approach.
# However, it has a very high dimensionality (a large number of cells and genes) which is difficult to visualize and perform downstream analysis.
# We can first use linear dimensionality reduction like PCA and then perform non-linear dimensionality reduction like t-SNE or UMAP
# and then use clustering algorithms to visualize.


