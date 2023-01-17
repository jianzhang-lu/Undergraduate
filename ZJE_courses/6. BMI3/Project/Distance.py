import numpy as np
import copy


class Distance:
    """
    This class Distance combines all relevant attributes used in calculating TCR distances and can call function self.Distance_Main() to calculate.
    The overall principle refers to the dynamic programming.

    :attribute trim: Whether or not to trim the conserved sequences
    :attribute BLOSUM: The BLOSUM matrix used in global alignment (62 or 80)
    :attribute open: The penalty points for a gap open
    :attribute extend: The penalty points for a gap extend
    :attribute weight: The percentage of CDR3b weight when calculating distance
    :attribute select: The top percentage of the distance from each TCR sequence to others will be considered when clustering
    """

    def __init__(self, BLOSUM, trim: bool, open: int, extend: int, weight: int, select: int):
        # The attribute amino_acid is corresponding with the BLOSUM matrix
        self.amino_acid = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V', 'B', 'Z', 'X']
        self.BLOSUM = BLOSUM
        self.trim = trim
        self.open = open
        self.extend = extend
        self.weight = weight
        self.select = select
        self.Transform_BLOSUM_Matrix()

    def Transform_BLOSUM_Matrix(self):
        """
        @brief:
            Transform the attribute BLOSUM (from 62 or 80 to BLOSUM Matrix)
        @returns:
            Self with the new set attribute BLOSUM
        """
        BLOSUM62 = [[4, -1, -2, -2, 0, -1, -1, 0, -2, -1, -1, -1, -1, -2, -1, 1, 0, -3, -2, 0, -2, -1, 0],
                    [-1, 5, 0, -2, -3, 1, 0, -2, 0, -3, -2, 2, -1, -3, -2, -1, -1, -3, -2, -3, -1, 0, -1],
                    [-2, 0, 6, 1, -3, 0, 0, 0, 1, -3, -3, 0, -2, -3, -2, 1, 0, -4, -2, -3, 3, 0, -1],
                    [-2, -2, 1, 6, -3, 0, 2, -1, -1, -3, -4, -1, -3, -3, -1, 0, -1, -4, -3, -3, 4, 1, -1],
                    [0, -3, -3, -3, 9, -3, -4, -3, -3, -1, -1, -3, -1, -2, -3, -1, -1, -2, -2, -1, -3, -3, -2],
                    [-1, 1, 0, 0, -3, 5, 2, -2, 0, -3, -2, 1, 0, -3, -1, 0, -1, -2, -1, -2, 0, 3, -1],
                    [-1, 0, 0, 2, -4, 2, 5, -2, 0, -3, -3, 1, -2, -3, -1, 0, -1, -3, -2, -2, 1, 4, -1],
                    [0, -2, 0, -1, -3, -2, -2, 6, -2, -4, -4, -2, -3, -3, -2, 0, -2, -2, -3, -3, -1, -2, -1],
                    [-2, 0, 1, -1, -3, 0, 0, -2, 8, -3, -3, -1, -2, -1, -2, -1, -2, -2, 2, -3, 0, 0, -1],
                    [-1, -3, -3, -3, -1, -3, -3, -4, -3, 4, 2, -3, 1, 0, -3, -2, -1, -3, -1, 3, -3, -3, -1],
                    [-1, -2, -3, -4, -1, -2, -3, -4, -3, 2, 4, -2, 2, 0, -3, -2, -1, -2, -1, 1, -4, -3, -1],
                    [-1, 2, 0, -1, -3, 1, 1, -2, -1, -3, -2, 5, -1, -3, -1, 0, -1, -3, -2, -2, 0, 1, -1],
                    [-1, -1, -2, -3, -1, 0, -2, -3, -2, 1, 2, -1, 5, 0, -2, -1, -1, -1, -1, 1, -3, -1, -1],
                    [-2, -3, -3, -3, -2, -3, -3, -3, -1, 0, 0, -3, 0, 6, -4, -2, -2, 1, 3, -1, -3, -3, -1],
                    [-1, -2, -2, -1, -3, -1, -1, -2, -2, -3, -3, -1, -2, -4, 7, -1, -1, -4, -3, -2, -2, -1, -2],
                    [1, -1, 1, 0, -1, 0, 0, 0, -1, -2, -2, 0, -1, -2, -1, 4, 1, -3, -2, -2, 0, 0, 0],
                    [0, -1, 0, -1, -1, -1, -1, -2, -2, -1, -1, -1, -1, -2, -1, 1, 5, -2, -2, 0, -1, -1, 0],
                    [-3, -3, -4, -4, -2, -2, -3, -2, -2, -3, -2, -3, -1, 1, -4, -3, -2, 11, 2, -3, -4, -3, -2],
                    [-2, -2, -2, -3, -2, -1, -2, -3, 2, -1, -1, -2, -1, 3, -3, -2, -2, 2, 7, -1, -3, -2, -1],
                    [0, -3, -3, -3, -1, -2, -2, -3, -3, 3, 1, -2, 1, -1, -2, -2, 0, -3, -1, 4, -3, -2, -1],
                    [-2, -1, 3, 4, -3, 0, 1, -1, 0, -3, -4, 0, -3, -3, -2, 0, -1, -4, -3, -3, 4, 1, -1],
                    [-1, 0, 0, 1, -3, 3, 4, -2, 0, -3, -3, 1, -1, -3, -1, 0, -1, -3, -2, -2, 1, 4, -1],
                    [0, -1, -1, -1, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, 0, 0, -2, -1, -1, -1, -1, -1]]

        BLOSUM80 = [[7, -3, -3, -3, -1, -2, -2, 0, -3, -3, -3, -1, -2, -4, -1, 2, 0, -5, -4, -1, -3, -2, -1],
                    [-3, 9, -1, -3, -6, 1, -1, -4, 0, -5, -4, 3, -3, -5, -3, -2, -2, -5, -4, -4, -2, 0, -2],
                    [-3, -1, 9, 2, -5, 0, -1, -1, 1, -6, -6, 0, -4, -6, -4, 1, 0, -7, -4, -5, 5, -1, -2],
                    [-3, -3, 2, 10, -7, -1, 2, -3, -2, -7, -7, -2, -6, -6, -3, -1, -2, -8, -6, -6, 6, 1, -3],
                    [-1, -6, -5, -7, 13, -5, -7, -6, -7, -2, -3, -6, -3, -4, -6, -2, -2, -5, -5, -2, -6, -7, -4],
                    [-2, 1, 0, -1, -5, 9, 3, -4, 1, -5, -4, 2, -1, -5, -3, -1, -1, -4, -3, -4, -1, 5, -2],
                    [-2, -1, -1, 2, -7, 3, 8, -4, 0, -6, -6, 1, -4, -6, -2, -1, -2, -6, -5, -4, 1, 6, -2],
                    [0, -4, -1, -3, -6, -4, -4, 9, -4, -7, -7, -3, -5, -6, -5, -1, -3, -6, -6, -6, -2, -4, -3],
                    [-3, 0, 1, -2, -7, 1, 0, -4, 12, -6, -5, -1, -4, -2, -4, -2, -3, -4, 3, -5, -1, 0, -2],
                    [-3, -5, -6, -7, -2, -5, -6, -7, -6, 7, 2, -5, 2, -1, -5, -4, -2, -5, -3, 4, -6, -6, -2],
                    [-3, -4, -6, -7, -3, -4, -6, -7, -5, 2, 6, -4, 3, 0, -5, -4, -3, -4, -2, 1, -7, -5, -2],
                    [-1, 3, 0, -2, -6, 2, 1, -3, -1, -5, -4, 8, -3, -5, -2, -1, -1, -6, -4, -4, -1, 1, -2],
                    [-2, -3, -4, -6, -3, -1, -4, -5, -4, 2, 3, -3, 9, 0, -4, -3, -1, -3, -3, 1, -5, -3, -2],
                    [-4, -5, -6, -6, -4, -5, -6, -6, -2, -1, 0, -5, 0, 10, -6, -4, -4, 0, 4, -2, -6, -6, -3],
                    [-1, -3, -4, -3, -6, -3, -2, -5, -4, -5, -5, -2, -4, -6, 12, -2, -3, -7, -6, -4, -4, -2, -3],
                    [2, -2, 1, -1, -2, -1, -1, -1, -2, -4, -4, -1, -3, -4, -2, 7, 2, -6, -3, -3, 0, -1, -1],
                    [0, -2, 0, -2, -2, -1, -2, -3, -3, -2, -3, -1, -1, -4, -3, 2, 8, -5, -3, 0, -1, -2, -1],
                    [-5, -5, -7, -8, -5, -4, -6, -6, -4, -5, -4, -6, -3, 0, -7, -6, -5, 16, 3, -5, -8, -5, -5],
                    [-4, -4, -4, -6, -5, -3, -5, -6, 3, -3, -2, -4, -3, 0, -6, -3, -3, 3, 11, -3, -5, -4, -3],
                    [-1, -4, -5, -6, -2, -4, -4, -6, -5, 4, 1, -4, 1, -2, -4, -3, 0, -5, -3, 7, -6, -4, -2],
                    [-3, -2, 5, 6, 6, -1, 1, -2, -1, -6, -7, -1, -5, -6, -4, 0, -1, -8, -5, -6, 6, 0, -3],
                    [-2, 0, -1, 1, -7, 5, 6, -4, 0, -6, -5, 1, -3, -6, -2, -1, -2, -5, -4, -4, 0, 6, -1],
                    [-1, -2, -2, -3, -4, -2, -2, -3, -2, -2, -2, -2, -2, -3, -3, -1, -1, -5, -3, -2, -3, -1, -2]]
        if self.BLOSUM == 62:
            self.BLOSUM = BLOSUM62
        if self.BLOSUM == 80:
            self.BLOSUM = BLOSUM80
        return

    def To_Match(self, seq1: str, seq2: str, i: int, j: int) -> int:
        """
        @brief:
            Look for the score corresponding to a position in the sequence.
        @args:
            seq1: The first sequence
            seq2: The second sequence
            i: The position of the seq1
            j: The position of the seq2
        @returns:
            The score of the two amino acid from the BLOSUM matrix.
        """

        # Get the position of the sequence amino acid in the list
        index_seq1 = self.amino_acid.index(seq1[i-1])
        index_seq2 = self.amino_acid.index(seq2[j-1])
        return self.BLOSUM[index_seq2][index_seq1]

    def Initial_X(self, i: int, j: int):
        """
        @brief:
            Initialize X Matrix
        @args:
            i: The position of the line
            j: The position of the column
        @returns:
            The initialization score for that location
        """

        if i > 0 and j == 0:
            return float("-inf")
        else:
            if j > 0 and i == 0:
                # return the score if every seat is empty
                return self.open + self.extend * (j-1)
            else:
                return 0

    def Initial_Y(self, i: int, j: int):
        """
        @brief:
            Initialize Y Matrix.
        @args:
            i: The position of the line
            j: The position of the column
        @returns:
            The initialization score for that location
        """

        if j > 0 and i == 0:
            return float("-inf")
        else:
            if i > 0 and j == 0:
                return self.open + self.extend * (i-1)
            else:
                return 0

    @staticmethod
    def Initial_M(i: int, j: int):
        """
        @brief:
            Initialize M Matrix.
        @args:
            i: The position of the line
            j: The position of the column
        @returns:
            The initialization score for that location
        """

        if i == 0 and j == 0:
            return 0
        else:
            if j == 0 or i == 0:
                return float("-inf")
            else:
                return 0

    def Calculate_Distance(self, seq1: str, seq2: str) -> int:
        """
        @brief:
            To calculate the max global alignment score of two sequences
        @args:
            seq1: The first sequence
            seq2: The second sequence
        @returns:
            The max score of the global alignment score between two sequences
        """

        # X is a vertical transformation, Y is a horizontal transformation, seq1 and j are horizontal, seq2 and i are vertical
        X = np.zeros((len(seq2)+1, len(seq1)+1))
        Y = np.zeros((len(seq2)+1, len(seq1)+1))
        M = np.zeros((len(seq2)+1, len(seq1)+1))

        # To initialize the X, Y, M matrix
        for i in range(len(seq2) + 1):
            for j in range(len(seq1) + 1):
                X[i][j] = self.Initial_X(i, j)
                Y[i][j] = self.Initial_Y(i, j)
                M[i][j] = self.Initial_M(i, j)

        # Iterate over the three matrices
        for j in range(1, len(seq1) + 1):
            for i in range(1, len(seq2) + 1):
                X[i][j] = max((self.open + M[i][j-1]), (self.extend + X[i][j-1]))
                Y[i][j] = max((self.open + M[i-1][j]), (self.extend + Y[i-1][j]))
                M[i][j] = max((self.To_Match(seq2, seq1, i, j) + M[i-1][j-1]),
                              self.To_Match(seq2, seq1, i, j) + X[i-1][j-1],
                              self.To_Match(seq2, seq1, i, j) + Y[i-1][j-1])

        # Return the last score in the M matrix as the best global alignment score
        return M[-1][-1]

    def Integrate_Distances(self, dataset: list) -> dict:
        """
        @brief:
            Calculate the distance between every two sequences and put them into a dictionary
        @args:
            dataset: The sequences to be aligned. Example value = [[CDR3b sequences]]
                     If we want to consider CDR3a, dataset = [[CDR3b sequences], [CDR3a sequences]]
        @returns:
            A dictionary containing every distance between every two sequences
        """

        # Judge whether the CDR3a sequences will be considered
        CDR3b = dataset[0]
        CDR3a = None
        if self.weight != 100:
            CDR3a = dataset[1]
            considerCDR3a = True
        else:
            considerCDR3a = False

        # Initialize the output dictionary
        distance_dic = {}
        for i in range(len(CDR3b)):
            distance_dic[i] = {}
            for j in range(len(CDR3b)):
                distance_dic[i][j] = 0

        for i in range(len(CDR3b)):
            # seq1 is the CDR3b of first TCR
            seq1 = CDR3b[i]
            seq3 = None
            # seq3 is the CDR3a of first TCR
            if considerCDR3a:
                seq3 = CDR3a[i]

            for j in range(len(CDR3b)):
                # seq2 is the CDR3b of second TCR
                seq2 = CDR3b[j]
                seq4 = None
                # seq4 is the CDR3a of second TCR
                if considerCDR3a:
                    seq4 = CDR3a[j]

                # Calculate the score using the weight.
                if considerCDR3a:
                    distance_dic[i][j] = round(self.Calculate_Distance(seq1, seq2)*(self.weight/100) +
                                               self.Calculate_Distance(seq3, seq4)*(1-self.weight/100), 1)
                else:
                    distance_dic[i][j] = round(self.Calculate_Distance(seq1, seq2), 1)

        return distance_dic

    def Adjust_Distances(self, dataset: list) -> dict:
        """
        @brief:
            For each TCR sequence, only record the top distances and corresponding sequences
        @args:
            dataset: The sequences to be aligned. Example value = [[CDR3b sequences]]
                     If we want to consider CDR3a, dataset = [[CDR3b sequences], [CDR3a sequences]]
        @returns:
            A dictionary which contains top distances between every two sequences
        """

        distance_dic = self.Integrate_Distances(dataset)
        length = len(dataset[0])
        select_top = int(length * self.select / 100)

        # Prepare a dictionary to record the top distance value of each point
        dic_sorted = {}
        for num1 in range(length):
            dic_sorted[num1] = {}

        for key in distance_dic:
            # Get the list for the distance from high to low
            sorted_list = sorted(distance_dic[key].items(), key=lambda d: d[1], reverse=True)

            # Rewrite the number of the range to set the top of the distance we want
            for num in range(select_top):
                if not sorted_list[num][0] == key:
                    dic_sorted[key][sorted_list[num][0]] = sorted_list[num][1]

        dic_sorted_add = copy.deepcopy(dic_sorted)
        for key in dic_sorted:
            for key1 in dic_sorted[key]:
                dic_sorted_add[key1][key] = dic_sorted[key][key1]
        return dic_sorted_add

    @staticmethod
    def Trim(dataset: list) -> list:
        """
        @brief:
            Trim TCR sequences
        @args:
            dataset: The sequences to be aligned. Example value = [[CDR3b sequences]]
                     If we want to consider CDR3a, dataset = [[CDR3b sequences], [CDR3a sequences]]
        @returns:
            Trimmed TCR sequences
        """
        new_dataset = []
        for i in dataset[0]:
            new_dataset.append(i[2: -2])
        dataset[0] = new_dataset
        return dataset

    def Distance_Main(self, dataset) -> dict:

        """
        @brief:
            Use the previously built functions to align the sequences
        @args:
            dataset: The sequences to be aligned. Example value = [[CDR3b sequences]]
            If we want to consider CDR3a, dataset = [[CDR3b sequences], [CDR3a sequences]]
        @returns:
            An output dictionary for clustering
        """

        print("--------------------------------------")
        print("Start Calculating Distances")
        print("--------------------------------------")

        # Start calculating
        if self.trim:
            dataset = self.Trim(dataset)
        dic_for_clustering = self.Adjust_Distances(dataset)
        print("End Calculating Distances")
        return dic_for_clustering

