import sympy
import random

def generate_keys(bit_length=1024):
    # Generate two large prime numbers p and q
    p = sympy.randprime(2**(bit_length//2 - 1), 2**(bit_length//2))
    q = sympy.randprime(2**(bit_length//2 - 1), 2**(bit_length//2))

    # Compute n (modulus) and phi(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Choose an integer e such that 1 < e < phi_n and gcd(e, phi_n) = 1
    e = 65537  # It's common to use 65537 as the public exponent

    # Compute the private key d, the modular multiplicative inverse of e modulo phi_n
    d = sympy.mod_inverse(e, phi_n)

    # Public key (e, n) and private key (d, n)
    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key

def encrypt(plaintext, public_key):
    e, n = public_key
    # Convert each character in the plaintext to its corresponding integer
    plaintext_integers = [ord(char) for char in plaintext]
    # Encrypt each integer using the public key
    ciphertext = [pow(char, e, n) for char in plaintext_integers]
    return ciphertext

def decrypt(ciphertext, private_key):
    d, n = private_key
    # Decrypt each integer in the ciphertext using the private key
    decrypted_integers = [pow(char, d, n) for char in ciphertext]
    # Convert each decrypted integer back to its corresponding character
    plaintext = ''.join(chr(char) for char in decrypted_integers)
    return plaintext

# Example usage
public_key, private_key = generate_keys()

plaintext = "apple"
print(f"Original plaintext: {plaintext}")

ciphertext = encrypt(plaintext, public_key)
print(f"Encrypted ciphertext: {ciphertext}")

decrypted_text = decrypt(ciphertext, private_key)
print(f"Decrypted text: {decrypted_text}")
