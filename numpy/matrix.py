import numpy as np

A = [[1,2,3], [1,2,3]]
print(A)

B = [[1,2], [1,2], [1,2]]
print(B)

A = np.array(A)
B = np.array(B)
C = A.dot(B)
print(C)
C = B.dot(A)
print(C)
