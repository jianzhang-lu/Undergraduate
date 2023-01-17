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


def Forward(transition: np.array, emission: np.array, observations: list):
    station = Stationary(transition)
    T = len(observations)
    N = np.shape(transition)[0]

    # 初始化forward的第一列(最底层)
    forward = np.zeros((N, T))
    o1 = observations[0]
    for state in range(N):
        forward[state, 0] = station[state] * emission[state, o1]

    # recursion step
    for step in range(1, T):
        o = observations[step]
        for cur_state in range(N):
            obser_p = emission[cur_state, o]
            for last_state in range(N):
                previous = forward[last_state, step-1]
                trans_p = transition[last_state, cur_state]
                forward[cur_state, step] += previous * trans_p * obser_p

    # termination step
    forward_p = np.sum(forward, axis=0)[T-1]
    return forward_p


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

print(Forward(transition, emission, observations))