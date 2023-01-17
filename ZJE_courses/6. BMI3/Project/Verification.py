import pandas as pd
import os

class Verification:
    """
    This class Verification is used when users set -ver or --verification.
    It combines all relevant attributes used in verification and can call function self.Ver_Main() to execute.
    The main goal of this process is to find the consensus motif of peptide in one cluster.

    :attribute amino_acid: The list of amino acids (the same as the attribute amino_acid in the Distance class
    :attribute cluster_info: The information of clustering
    :attribute CDR3b: The sequence of CDR3b
    :attribute peptide: The sequence of corresponding epitope peptide
    :attribute output: The title name of the output file
    """

    def __init__(self, cluster_info, CDR3b, peptide, output_file):
        self.amino_acid = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V', 'B', 'Z', 'X']
        self.cluster_info = cluster_info
        self.CDR3b = CDR3b
        self.peptide = peptide
        self.output = output_file

    def Profile(self, motifs: list) -> pd.DataFrame:
        """
        @brief:
            Generate the overall profile of motifs
        @args:
            motifs: the list of all motifs
        @returns:
            The profile dataframe
        """

        aa_list = self.amino_acid
        k_len = len(motifs[0])
        count_result = [[1] * k_len for _ in range(len(aa_list))]
        for motif in motifs:
            for i, n in enumerate(motif):
                count_result[aa_list.index(n)][i] += 1
        count_frame = pd.DataFrame(count_result)
        dna_sum = count_frame.sum(axis=0)
        profile_result = count_frame.div(dna_sum)
        profile_result.index = aa_list
        return profile_result

    def Output_File(self, consensus_info):
        """
        @brief:
            Output the result of verification
        @returns:
            A csv file containing the clustering information, consensus motif information
        """

        # Generate the cluster information, CDR3 and peptide columns.
        out_cluster = []
        out_CDR3 = []
        out_peptide = []
        out_consensus = []

        for index, community in enumerate(self.cluster_info):
            for seq in community:
                out_cluster.append(index)
                out_CDR3.append(self.CDR3b[seq])
                out_peptide.append(self.peptide[seq])
                out_consensus.append(consensus_info[index])

        # Write into the file

        filename = self.output+'.csv'

        file = pd.DataFrame({'Community': out_cluster,
                             'CDR3b': out_CDR3,
                             'Peptide': out_peptide,
                             'Consensus': out_consensus})

        if os.path.exists(filename):
            os.remove(filename)
        file.to_csv(filename)
        return

    def Ver_Main(self):
        """
        @brief:
            Main function in this class, generate consensus motif for each community and output files.
        @returns:
            A csv file containing the clustering information, consensus motif information
        """

        print("--------------------------------------")
        print("Start Verification")
        print("--------------------------------------")

        consensus_info = []
        # Calculate consensus motif in each community
        for community in self.cluster_info:
            one_cluster_peptides = [self.peptide[i] for i in community]

            # Calculate the min length in these peptides
            min_len = min([len(i) for i in one_cluster_peptides])
            # Trim peptides
            new_peptides = [i[: min_len] for i in one_cluster_peptides]

            # Find the consensus motif
            profile = self.Profile(new_peptides)
            consensus_motif = ''.join(list(profile.idxmax()))
            consensus_info.append(consensus_motif)
        self.Output_File(consensus_info)
        print("End Verification")
        return
