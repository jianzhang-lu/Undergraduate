tower_dict = ['X', 'A', 'B', 'C']
def HanoiTowers(n, fromPeg, toPeg):
    if n == 1:
        print('Move disk', n, 'from rod', tower_dict[fromPeg], 'to rod', tower_dict[toPeg])
        return

    unusedPeg = 6-fromPeg-toPeg
    HanoiTowers(n-1, fromPeg, unusedPeg)
    print('Move disk', n, 'from rod', tower_dict[fromPeg], 'to rod', tower_dict[toPeg])
    HanoiTowers(n-1, unusedPeg, toPeg)


HanoiTowers(4, 1, 3)