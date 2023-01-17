# test.py
import argparse

from mountain import *

DNA = [
    'TTACCTTAAC', 
    'GATGTCTGTC', 
    'ACGGCGTTAG', 
    'CCCTAACGAG', 
    'CGTCAGAGGT'
]

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='ECE448 MP1 Search')

    parser.add_argument('--test', choices = ["mountain", "motif", "all"],
                        help='test problem1 or problem2')
    parser.add_argument('--human', default = False, action = "store_true",
                        help='flag for human visualization of the terrain')
    parser.add_argument('--dim', default = 2, type=int, choices = [2,3],
                        help='dimension of the human readable plot')
    parser.add_argument('--file', help='mountain file to test')
    parser.add_argument('--level', default=20, type=int)

    args = parser.parse_args()

    if args.test == "mountain":
        from findpath import *
        m = Mountain(args.file)
        path = greedy(m)
        print("The path cost <time: {}> to reach the goal".format(m.calculatePath(path)))
        if args.human:
            import matplotlib.pyplot as plt

            if args.dim == 2:
                fig,ax = plt.subplots(1,2)
                m.plotContour(ax = ax[0], level = args.level)
                m.plotContour(ax = ax[1], level = args.level)
                m.plotPath(ax[1], path)
            else:
                fig,ax = plt.subplots(2,2)
                m.plotContour(ax = ax[0][0])
                m.plotContour(ax = ax[0][1])
                m.plotPath(ax[0][1], path)
                ax[1][0].set_axis_off()
                ax[1][1].set_axis_off()
                ax = fig.add_subplot(223, projection="3d")
                ax.set_axis_off()
                m.plot3D(ax = ax)
                ax = fig.add_subplot(224, projection="3d")
                m.plot3D(ax = ax)
                ax.set_axis_off()
                m.plot3DPath(ax, path)
                plt.show()
              
            plt.show()
    if args.test == "motif":
        from motif import *
        print("Your motif result of 3-mer is {}".format(GreedyMotifSearch(DNA, 3, len(DNA))))
        print("Your motif result of 4-mer is {}".format(GreedyMotifSearch(DNA, 4, len(DNA))))
        print("Your motif result of 5-mer is {}".format(GreedyMotifSearch(DNA, 5, len(DNA))))