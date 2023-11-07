import numpy as np
from py_ecc.bn128 import curve_order, field_modulus, G1, multiply, eq

# define the matrices
A = np.array([[0, 0, 0, 0, 3, 0],
              [0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 5, 0]])
              
B = np.array([[0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 1]])
              
C = np.array([[0, 0, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [(-3 % curve_order), 1, 0, (-1 % curve_order), 1, 2]])

# create the witness vector
witness = np.array([1, 61, 12, 36, 2, 3])

# Multiplication is element-wise, not matrix multiplication. # Result contains a bool indicating an element-wise indicator that the equality is true for that element.
result = (C.dot(witness) % curve_order) == ((A.dot(witness) % curve_order) * (B.dot(witness) % curve_order)) % curve_order
print(result)

#print("C: ", C.dot(witness))
#print("A: ", A.dot(witness))
#print("B: ", B.dot(witness))
#print("A times B", A * B)

# check that every element-wise equality is true
#assert result.all(), "result contains an inequality"