import numpy as np

def equilibrium(A, T=1000):
    basis = np.eye(len(A))
    p = np.array(basis[0], dtype='float64')
    q = np.array(basis[0], dtype='float64')
    
    for t in range(T):
        alpha = 2 / (2 + t)
        dp = np.dot(A, q)
        i = np.argmax(dp)
        p += alpha * (basis[i] - p)
        dq = np.dot(p, A)
        j = np.argmin(dq)
        q += alpha * (basis[j] - q)

    return p, q
