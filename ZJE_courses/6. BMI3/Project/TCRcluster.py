import argparse
import pandas as pd
from Distance import Distance
from Cluster import Cluster
from Plotting import Visualization_Main
from Verification import Verification


def Parse_args():
    """
    @brief: Use argparse to make the code command-line executable
    @returns: Parsed arguments
    """
    parser = argparse.ArgumentParser(prog='TCRcluster.py',
                                     description='You can specify those parameters or use their default values.',
                                     epilog='You can read the documentation for detailed explanation and some examples.')

    # 1. About the input file.
    parser.add_argument('-i', '--input',
                        metavar='',
                        help='The path and name of the input file. It must contain at least 1 column with the fixed name: CDR3b.\n'
                             'It represents the sequences of CDR3b on the β chain of T cells.\n'
                             'If you want to consider the sequences of CDR3a on the α chain of T cells, '
                             'the input file must also contain the CDR3a column representing the sequences of CDR3a.\n'
                             'If you want to verify the result of TCR clustering using the corresponding epitope sequences, '
                             'the input file must also contain the peptide column representing the epitope sequences.',
                        required=True)

    parser.add_argument('-t', '--trim',
                        help='Whether to trim the conserved sequences of CDR3b (2 amino acids on the N-terminal side and the C-terminal side).\n'
                             'If this parameter is added, these conserved sequences will be trimmed.',
                        action="store_true")

    # 2. About the distance calculation
    parser.add_argument('-B', '--BLOSUM',
                        metavar='',
                        choices=[62, 80],
                        help='The BLOSUM matrix used in global alignment to assign points for matched/mismatched amino acid.\n'
                             'Must be 62 or 80 (default 62).',
                        default=62,
                        type=int)

    parser.add_argument('-e', '--extend',
                        metavar='',
                        help='The penalty points for a gap extend (default -1).',
                        default=-1,
                        type=int)

    parser.add_argument('-o', '--open',
                        metavar='',
                        help='The penalty points for a gap open (default -5).',
                        default=-5,
                        type=int)

    parser.add_argument('-w', '--weight',
                        metavar='',
                        choices=range(0, 101),
                        help='The percentage of CDR3b weight when calculating distance between each TCR sequence.\n'
                             'This value must be integers from 0 to 100 (default 100). "100" means only the CDR3b sequence will be considered.',
                        default=100,
                        type=int)

    # 3. About the clustering
    parser.add_argument('-s', '--select',
                        metavar='',
                        choices=range(1, 51),
                        help='Only the top percentage of the distance from each TCR sequence to others will be considered when clustering.\n'
                             'This value must be integers from 1 to 50 (default 10).\n'
                             'A bigger percentage may conclude a more convincing conclusion but with a much longer running time.',
                        default=10,
                        type=int)

    # 4. About the verification
    parser.add_argument('-ver', '--verification',
                        help='Whether to verify the result of TCR clustering using the corresponding epitope sequences.\n'
                             'If this parameter is added, a csv file showing the verification will be output.',
                        action="store_true")

    # 5. About the output path and files
    parser.add_argument('-out', '--output',
                        metavar='',
                        help='The path and file title name for outputs.',
                        required=True,
                        type=str)

    args = parser.parse_args()
    return args


def TCRcluster():
    """
    @brief: Main functions combining all other classes
    @returns: Output files including a clustering plot, a clustering information and a verification information (if users set -ver)
    """

    args = Parse_args()
    file = pd.read_csv(args.input)
    CDR3a = None
    peptide = None

    # Test whether the form of input file is correct
    try:
        CDR3b = file['CDR3b']
    except KeyError:
        print('Error! The file must have the CDR3b column.')
        return

    if args.verification:
        try:
            peptide = file['peptide']
        except KeyError:
            print('Error! You want to verify the result of TCR clustering, so the file must have the peptide column.')
            return

    if args.weight != 100:
        try:
            CDR3a = file['CDR3a']
        except KeyError:
            print('Error! You want to verify the result of TCR clustering, so the file must have the peptide column.')
            return

    # If the form of input file is correct, then start running the codes.
    if args.weight != 100:
        dataset = [list(CDR3b), list(CDR3a)]
    else:
        dataset = [list(CDR3b)]

    distance = Distance(args.BLOSUM, args.trim, args.open, args.extend, args.weight, args.select).Distance_Main(dataset)
    cluster = Cluster(distance, args.output).Cluster_Main()
    if args.verification:
        Verification(cluster, CDR3b, peptide, args.output).Ver_Main()
    Visualization_Main(distance, cluster, args.output)
    return


if __name__ == '__main__':
    TCRcluster()