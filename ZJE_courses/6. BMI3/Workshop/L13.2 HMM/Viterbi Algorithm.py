import numpy as np

def Stationary(A: np.array):
    # 初始化
    stationary_state = np.zeros(np.shape(A)[0])
    test_state = np.zeros(np.shape(A)[0])
    stationary_state[0] = 1
    while True:
        stationary_state = np.dot(stationary_state, A)
        if (test_state == stationary_state).all():
            break
        test_state = stationary_state
    return stationary_state


# 根据observation 找到最符合的sequence of hidden states
def Viterbi(transition: np.array, emission: np.array, observations: list):
    station = Stationary(transition)
    T = len(observations)
    N = np.shape(transition)[0]

    # 初始化forward的第一列(最底层) 以及backpointer回溯
    viterbi = np.zeros((N, T))
    backpointer = np.zeros((N, T))
    o1 = observations[0]
    for state in range(N):
        viterbi[state, 0] = station[state] * emission[state, o1]

    # recursion step
    for step in range(1, T):
        o = observations[step]
        for cur_state in range(N):
            values = []
            obser_p = emission[cur_state, o]
            for last_state in range(N):
                previous = viterbi[last_state, step-1]
                trans_p = transition[last_state, cur_state]
                values.append(previous * trans_p * obser_p)

            # 找到values中最大的值和其对应的last_state
            viterbi[cur_state, step] = max(values)
            backpointer[cur_state, step] = values.index(max(values))
    print(backpointer)

    # termination step
    best_p = np.max(viterbi, axis=0)[T-1]
    best_pointer = np.argmax(viterbi, axis=0)[T-1]

    # 回溯过程
    path = [best_pointer]
    counter = T-1
    while counter > 0:
        best_pointer = backpointer[int(best_pointer), counter]
        path.insert(0, best_pointer)
        counter -= 1

    return round(best_p, 2), list(map(int, path))

# xyz是observation, AB是state
# transition相当于{'A': {'A': 0.641, 'B': 0.359},
#                 'B': {'A': 0.729, 'B': 0.271}}
# row为last col为next
transition = np.array([[0.641, 0.359],
                       [0.729, 0.271]])

# emission相当于{'A': {'x': 0.117, 'y': 0.691, 'z': 0.192},
#               'B': {'x': 0.097, 'y': 0.42, 'z': 0.483}}
emission = np.array([[0.117, 0.691, 0.192],
                     [0.097, 0.42, 0.483]])

state = ['A', 'B']
character = ['x', 'y', 'z']
sequence = 'xyxzzxyxyy'
observations = []
for i in sequence:
    observations.append(character.index(i))

res = Viterbi(transition, emission, observations)[1]
print(res)
for r in res:
    print(state[r], end='')


