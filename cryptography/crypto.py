#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   crypto.py
@Contact :   sroy10@uh.edu
@Desc    :   This program shows examples of a/symmetric key cryptography
'''


from Cryptodome.Cipher import AES
# from Crypto.Cipher import AES         # does not work
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


# class for symmetric key crypto (AES)
class symmetricKeyCrypto:
    def encryption(self, plaintext, key):
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        iv = cipher.nonce
        return (ciphertext, iv, tag)
    
    def decryption(self, ciphertext, key, iv, tag):
        cipher = AES.new(key, AES.MODE_EAX, nonce=iv)
        decrypted = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted


# class for asymmetric key crypto (RSA)
class asymmetricKeyCrypto:
    def encryption(self, plaintext, public_key):
        ciphertext = public_key.encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext

    def decryption(self, ciphertext, private_key):
        decrypted = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted

if __name__ == "__main__":
    # Example usage of symmetric key cryptography
    key = get_random_bytes(16)
    plaintext = b'Hello World!'
    symm_crypto = symmetricKeyCrypto()

    ciphertext, iv, tag = symm_crypto.encryption(plaintext, key)
    decrypted = symm_crypto.decryption(ciphertext, key, iv, tag)

    print(f"\nSymmetric key encryption:\n")
    print(f"Plaintext: {plaintext}")
    print(f"Ciphertext: {ciphertext}")
    print(f"Decrypted: {decrypted}")
    

    # Example usage of asymmetric key cryptography
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    plaintext = b'Hello World!'
    asymm_crypto = asymmetricKeyCrypto()

    ciphertext = asymm_crypto.encryption(plaintext, public_key)
    decrypted = asymm_crypto.decryption(ciphertext, private_key)

    print(f"\nAsymmetric key encryption:\n")
    print(f"Plaintext: {plaintext}")
    print(f"Ciphertext: {ciphertext}")
    print(f"Decrypted: {decrypted}")
