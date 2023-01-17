# #!/usr/bin/python3
#
# ################
# # Question 1.1 #
# ################
#
# def reverseComplement(s: str) -> str:
#     '''
#     Returns the reverse complement of a DNA string (10 points)
#     Example input:
#         "AAAACCCGGT"
#     Example output:
#         "ACCGGGTTTT"
#     '''
#     # YOUR CODE HERE
#     return
#
# ################
# # Question 1.2 #
# ################
#
# def sortDNASequenceByLength(seqs: list) -> str:
#     '''
#     Returns the sorted list of DNA string by length (10 points)
#     Example input:
#         ['ATACAGA','AAGA','CTAGAGTCCAG','TTACCAGG','GAGAG','CTC']
#     Example output:
#         ['CTC','AAGA','GAGAG','ATACAGA','TTACCAGG', 'CTAGAGTCCAG']
#     '''
#     return
#
#
# ################
# # Question 2.1 #
# ################
#
# def findCodon(sequence:str) -> dict:
#     '''
#     Returns the possible transcriptional starting site from a DNA sequence
#     (15 points)
#     Example input:
#         "AAACATGTTATTGAGCTTAAAGTTGCAAAAATAAACTCATGTACCATAATTCATGAGTAGAAAAA
#         TAGACTAGTGGAATAACATAAAAATAAAAACAATGCTTACATAAAATGTTGTAACTGATTTGGATG
#         TCATTAGAAATCAGTAAGTAAATAG"
#     Example output:
#         {
#             "ATG": {128, 97, 4, 38, 110, 52},
#             "TAA": {106, 78, 46, 17, 145, 83, 116, 149, 89, 31},
#             "TAG": {65, 153, 70, 135, 57},
#             "TGA": {120, 11, 53}
#         }
#     '''
#     return
#
# ################
# # Question 2.2 #
# ################
#
# # Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val:int, left=None, right=None):
#         self.val = val self.left = left self.right = right
#     def insert(self, val:int):
#         # YOUR CODE HERE
#     def inorderTraversal(self):
#         # YOUR CODE HERE
#
# def treeSort(lst: list) -> list:
#     '''
#     returns a sorted list using the tree sort algorithm (15 points)
#     Example input:
#         [3, 10, 13, 5, 12, 19, 18, 15, 11, 4, 0, 16, 6, 9]
#     Exmaple output:
#         [0, 3, 4, 5, 6, 9, 10, 11, 12, 13, 15, 16, 18, 19]
#     '''
#     root = TreeNode()
#     for val in lst:
#         root.insert(val)
#     return root.inorderTraversal()
#
#
# ################
# # Question 3.1 #
# ################
#
# def DLDistance(a:str,b:str) -> int
#     '''
#     return the Damerau-Levenshtein distance (20 points)
#     Example input:
#         a = "CTCATGTACCATAAT"
#         b = "ACTTATACGATAATC"
#     Example output:
#         6
#     '''
#     return
#
# ################
# # Question 3.2 #
# ################
#
# def connectedComponents(components:list) -> list:
#     '''
#     given a list of two connected nodes in the graph, return the connected
#     components in the format of a nested list (20 points)
#     Example input:
#         [["v1","v2"]
#          ["v1","v3"]
#          ["v1","v4"]
#          ["v2","v3"]
#          ["v2","v4"]
#          ["v3","v4"]
#          ["v5","v6"]
#          ["v6","v7"]
#          ["v7","v8"]
#          ["v9","v10"]
#          ["v9","v11"]
#          ["v9","v12"]]
#     Example output:
#         [["v1", "v2", "v3", "v4"],
#          ["v5", "v6", "v7", "v8"],
#          ["v9", "v10", "v11", "v12"]]
#     '''
#
#     return
#
# ################
# # Question 4.1 #
# ################
#
# def exonChaining(intevals:list) -> int:
#     '''
#     Given a set of putative exons, find a maximum chain of non-overlapping putative exons
#     Exmaple input:
#         [(2,3), (1,5), (4,8), (9,10), (11,15), (13,14), (16,18)]
#     Example output:
#         5
#     '''
#
# ################
# # Question 4.2 #
# ################
#
# path = {
#     "22": {
#         "23": 10,
#         "15": 12,
#         "12": 13
#     },
#     "23": {
#         "22": 10,
#         "20": 15
#     },
#     "15": {
#         "20": 5,
#         "22": 12,
#         "12": 4,
#         "19": 7,
#         "11": 8
#     },
#     "12": {
#         "15": 4,
#         "11": 7
#     },
#     "20": {
#         "23": 15,
#         "21": 3,
#         "15": 5,
#         "19": 1
#     },
#     "18": {
#         "21": 2,
#         "19": 3,
#         "16": 4
#     },
#     "21": {
#         "18": 2,
#         "20": 3
#     },
#     "19": {
#         "20": 1,
#         "18": 3,
#         "15": 7,
#         "16": 4
#     },
#     "16": {
#         "18": 4,
#         "19": 4,
#         "11": 12,
#         "4": 5
#     },
#     "11": {
#         "16": 12,
#         "15": 8,
#         "10": 8,
#         "12": 7
#     },
#     "4": {
#         "16": 5,
#         "10": 8,
#         "2E": 3
#     },
#     "10": {
#         "4": 8,
#         "2E": 5,
#         "11": 8
#     },
#     "2E": {
#         "4": 3,
#         "10": 5,
#         "2A": 3
#     },
#     "2A": {
#         "2E": 3
#     }
# }
#
#  def shortestPath(path, source = 11, target = '2A'):
#     '''
#     Find the shortest path from Hospital ("22") to ZJE Building ("2E").
#     '''
#     return
#
# ################
# # Question 5.1 #
# ################
#
# import pandas as pd
# import numpy as np
# expressions = pd.read_csv("bmi3_umap.csv", header=None).to_numpy()
# def KMeans(n_clusters:int, iter:int, expressions: numpy.ndarray):
#     '''
#     Implement the Kmeans algorithm to find different clusters.
#     '''
#     return labels
#
#
# # labels is the result of your function
# plt.scatter(x=expressions[:,0], y=expressions[:,1],c=labels ,s=2)
#
#
# ################
# # Question 5.2 #
# ################
#
#
# def pentominoMutations(pent):
#     '''
#     Implement a function that find all mutations of a given pentomino.
#     Example input:
#         np.array([[0,1,1],
#                   [1,1,0],
#                   [0,1,0]])
#
#     Example output:
#         np.array([[[0, 1, 1],
#                   [1, 1, 0],
#                   [0, 1, 0]],
#
#                  [[1, 1, 0],
#                   [0, 1, 1],
#                   [0, 1, 0]],
#
#                  [[0, 1, 0],
#                   [1, 1, 0],
#                   [0, 1, 1]],
#
#                  [[1, 0, 0],
#                   [1, 1, 1],
#                   [0, 1, 0]],
#
#                  [[0, 1, 0],
#                   [1, 1, 1],
#                   [1, 0, 0]],
#
#                  [[0, 1, 0],
#                   [0, 1, 1],
#                   [1, 1, 0]],
#
#                  [[0, 1, 0],
#                   [1, 1, 1],
#                   [0, 0, 1]],
#
#                  [[0, 0, 1],
#                   [1, 1, 1],
#                   [0, 1, 0]]])
#
#     '''
#     return