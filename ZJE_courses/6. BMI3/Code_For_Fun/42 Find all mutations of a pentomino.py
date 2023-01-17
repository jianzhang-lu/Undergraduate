import numpy as np
def FindMutations(pentomino: list):
    final_res = []
    matrix = np.array(pentomino)
    matrix_flip = np.flip(pentomino, axis=1)
    for _ in range(4):
        final_res.append(matrix)
        matrix = np.rot90(matrix)
    for _ in range(4):
        final_res.append(matrix_flip)
        matrix_flip = np.rot90(matrix_flip)
    return [i.tolist() for i in final_res]


test = [[0, 1, 1], [1, 1, 0], [0, 1, 0]]
print(FindMutations(test))


