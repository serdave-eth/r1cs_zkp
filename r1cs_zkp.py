import numpy as np
from py_ecc.bn128 import add, curve_order, field_modulus, G1, G2, multiply, eq, pairing

def multiply_vector(G, w):
    return [multiply(G, wi) for wi in w]

def encrypt_matrix_rows(witness_G1, L):
    """
    Encrypts the sum of each row in matrix L by multiplying each element
    with the corresponding element in witness_G1 and then adding them up.

    :param witness_G1: A list or 1D NumPy array of encrypted witness values.
    :param L: A 2D NumPy array representing the matrix to encrypt.
    :return: A list of lists, with each sublist containing the encrypted sum of a row in L.
    """
    L_sum_encrypted = []

    for row in L:
        row_sum_encrypted = add(multiply(witness_G1[0], row[0]), multiply(witness_G1[1], row[1]))  # Start with the first two elements
        for i in range(2, len(row)):
            row_sum_encrypted = add(row_sum_encrypted, multiply(witness_G1[i], row[i]))
        L_sum_encrypted.append([row_sum_encrypted])

    return L_sum_encrypted

def verify_proof(L, R, O, witness_G1, witness_G2, G1, G2):

    """
    Verifies that the prover knows a solution to L*R = O without revealing the solution.

    Solution is encrypted on elliptic curves G1 and G2 via witness_G1, witness_G2

    Verifier checks L*R = O using elliptic curve pairings. (ab = cd where D = 1)

    """

    # Compute dot product L*witness, R*witness and O*witness
    L_sum_encrypted = encrypt_matrix_rows(witness_G1, L)
    R_sum_encrypted = encrypt_matrix_rows(witness_G2, R)
    O_sum_encrypted = encrypt_matrix_rows(witness_G1, O)

    # Verify witness encrypted EC G1 and G2 have the same pre-image
    for i in range(len(witness_G1)):
        if pairing(G2, witness_G1[i]) != pairing(witness_G2[i], G1):
            return False  # Proof failed

    # Verify pairings that prove L*R = O
    for i in range(len(L_sum_encrypted)):
        proof_LR = pairing(R_sum_encrypted[i][0], L_sum_encrypted[i][0])
        proof_O = pairing(G2, O_sum_encrypted[i][0])
        if proof_LR != proof_O:
            return False  # Proof failed

    # All proofs have passed
    return True

# Verifier: create the L, R and O matrices
L = np.array([[0, 0, 0, 0, 3, 0],
              [0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 5, 0]])
              
R = np.array([[0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 1]])
              
O = np.array([[0, 0, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [(-3 % curve_order), 1, 0, (-1 % curve_order), 1, 2]])

# Prover: create the witness vector
witness = np.array([1, 61, 12, 36, 2, 3])

# Prover: encrypt witness with G1 and G2 elliptic curves
witness_G1 = multiply_vector(G1, witness)
witness_G2 = multiply_vector(G2, witness)

# Verifier: verify encrypted witness is a valid solution to L*R = O
print(verify_proof(L, R, O, witness_G1, witness_G2, G1, G2))