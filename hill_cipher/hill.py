from ast import mod
import numpy as np
from math import sqrt, ceil

def key2matrix(key: str) -> np.ndarray:
    n = round(len(key) ** 0.5)
    key_matrix = np.array([ord(c) - ord('A') for c in key]).reshape(n, n)
    # print(key_matrix)
    return key_matrix

def matrix2key(matrix: np.ndarray) -> str:
    # print(matrix)
    return ''.join([chr(int(c) + ord('A')) for c in matrix.flatten()])

def mod_inverse(matrix, modulus):
    det = round(np.linalg.det(matrix))
    det_inv = pow(det, -1, modulus)
    cofactor_matrix = (np.linalg.inv(matrix).T * det)
    cofactor_matrix = np.round(cofactor_matrix).astype(int) % modulus
    mod_inv = (cofactor_matrix * det_inv) % modulus
    mod_inv = mod_inv.T
    return mod_inv

def encrypt(text: str, key: np.ndarray) -> str:
    n = key.shape[0]
    
    # Pad the text with 'X' if its length is not a multiple of n
    if len(text) % n != 0:
        text += 'X' * (n - len(text) % n)
    
    # Convert text to numeric array (A=0, B=1, ..., Z=25)
    data = np.array([ord(c) - ord('A') for c in text]).reshape(-1, n).T
    
    # Encrypt by multiplying the key matrix with the data matrix
    encrypted = np.dot(key, data) % 26
    
    # Flatten the encrypted matrix and convert back to characters
    encrypted = encrypted.T.flatten()
    encrypted_text = ''.join([chr(int(c) + ord('A')) for c in encrypted])
    
    return encrypted_text

def get_key(text: str, cipher: str) -> np.ndarray:
    working_text = text[:9]
    working_cipher = cipher[:9]
    # print(cipher, text)
    plain_text_vector = np.array([ord(c) - ord('A') for c in working_text]).reshape(3, 3).T
    cipher_text_vector = np.array(object=[ord(c) - ord('A') for c in working_cipher]).reshape(3, 3).T
    # print(working_text)
    # print(plain_text_vector)
    # print(working_cipher)
    # print(cipher_text_vector)
    # print(mod_inverse(plain_text_vector, 26))

    key = (cipher_text_vector @ mod_inverse(plain_text_vector, 26)) % 26
    # print(matrix2key(np.matmul(mod_inverse(plain_text_vector, 26), cipher_text_vector) % 26))
    # print(key)
    return matrix2key(key)

# data = 'ACT'
# key_matrix = key('GYBNQKURP')
# encrypted = encrypt(data, key_matrix)
# print(encrypted)

# print(get_key('ACT', encrypted))
# print(encrypt('ACT', key(get_key('ACT', encrypted))))

# EKXBRYMRALE FCWNKUCECKLX YSVQYUVVC

# data = 'EKXBRYMRALE'
# key_matrix = key2matrix('YSVQYUVVC')
# encrypted = encrypt(data, key_matrix)
# print("Encrypted text:", encrypted)

# discovered_key = get_key('EKXBRYMRALE', encrypted)
# print("Discovered Key: ", discovered_key)

# # Encrypt again using the discovered key to verify
# re_encrypted = encrypt(data, key2matrix(discovered_key))
# print("Re-encrypted text:", re_encrypted)
