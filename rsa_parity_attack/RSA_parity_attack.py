# import the necessary libraries here
from turtle import st
from Crypto.Util import number
from Crypto.Util.number import long_to_bytes, bytes_to_long

class RSA:
    """Implements the RSA public key encryption / decryption."""

    def __init__(self, key_length):
        # define self.p, self.q, self.e, self.n, self.d here based on key_length
        self.p = number.getPrime(key_length // 2)
        self.q = number.getPrime(key_length // 2)
        self.n = self.p * self.q
        self.e = 65537
        self.d = number.inverse(self.e, (self.p-1)*(self.q-1))

    def encrypt(self, binary_data):
        # return encryption of binary_data here
        m = bytes_to_long(binary_data)
        c = pow(m, self.e, self.n)
        return c

    def decrypt(self, encrypted_int_data):
        # return decryption of encrypted_binary_data here
        m = pow(encrypted_int_data, self.d, self.n)
        return long_to_bytes(m)

class RSAParityOracle(RSA):
    """Extends the RSA class by adding a method to verify the parity of data."""

    def is_parity_odd(self, encrypted_int_data):
        # Decrypt the input data and return whether the resulting number is odd
        decrypted_data = self.decrypt(encrypted_int_data)
        return decrypted_data[-1] % 2 == 1


def parity_oracle_attack(ciphertext, rsa_parity_oracle):
    # implement the attack and return the obtained plaintext
    n = rsa_parity_oracle.n
    e = rsa_parity_oracle.e
    c = ciphertext

    k = n.bit_length()

    if n % 2 == 0:
        d = pow(e, -1, n/2 - 1)
        return long_to_bytes(pow(c, d, n)).decode()

    left = 0
    right = n-1

    middle = (left + right) // 2

    power = pow(2, e, n)
    steps = 0
    while left < right:
        if rsa_parity_oracle.is_parity_odd((c * power) % n):
            left = middle + 1
        else:
            right = middle
        middle = (left + right) // 2
        power *= pow(2, e, n)
        steps += 1
    print(steps)
    print(middle)
    # for i in range(max(0, left-1000), left+1000):
    #     if pow(i, e, n) == c:
    #         print("Found")
    #         return long_to_bytes(i).decode()
    return long_to_bytes(left).decode()




def main():
    input_bytes = input("Enter the message: ")

    # Generate a 1024-bit RSA pair    
    rsa_parity_oracle = RSAParityOracle(key_length=1024)

    # Encrypt the message
    ciphertext = rsa_parity_oracle.encrypt(input_bytes.encode())
    print("Encrypted message is: ",ciphertext)
    # print("Decrypted text is: ",rsa_parity_oracle.decrypt(ciphertext))

    # Check if the attack works
    plaintext = parity_oracle_attack(ciphertext, rsa_parity_oracle)
    print("Obtained plaintext: ",plaintext)
    assert plaintext == input_bytes.encode()


if __name__ == '__main__':
    main()