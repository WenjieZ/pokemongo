import numpy as np

def equilibrium(A, T=1000):
    m, n = A.shape
    basis1, basis2 = np.eye(m), np.eye(n)
    p = np.array(basis1[0], dtype='float64')
    q = np.array(basis2[0], dtype='float64')
    
    for t in range(T):
        alpha = 2 / (2 + t)
        dp = np.dot(A, q)
        i = np.argmax(dp)
        p += alpha * (basis1[i] - p)
        dq = np.dot(p, A)
        j = np.argmin(dq)
        q += alpha * (basis2[j] - q)

    return p, q
