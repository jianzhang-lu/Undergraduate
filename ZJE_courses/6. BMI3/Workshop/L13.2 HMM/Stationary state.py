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


A = np.array([[0.2, 0.6, 0.2],
              [0.3, 0, 0.7],
              [0.5, 0, 0.5]])
print(Stationary(A))