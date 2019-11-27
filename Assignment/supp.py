import numpy as np
from scipy.linalg import solve

lam = 1/600
miu_l = 1/60
miu_t = 1/90

A = np.array([[1, 1, 1, 1, 1, 1], 
		     [4*lam, -miu_t, -miu_l, 0, 0, 0], 
	         [4*lam, -(miu_t+3*lam), 0, miu_l, 0, 0], 
		     [0, 3*lam, 3*lam, -(miu_l+miu_t+2*lam), (miu_l+miu_t), 0],
		     [0, 0, 0, 0, lam, -(miu_l+miu_t)],
		     [0, 0, (miu_l+3*lam), - miu_t, 0, 0]])

B = np.array([1, 0, 0, 0, 0, 0])

result = solve(A, B)
print(result)
