from error import *
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

key = bytes.fromhex('7a231e74a1771acbdb2161b550901242204a2fdab78a87801081d26f49dd0651') #hard coded encryption key for developing
#key = secrets.token_bytes(32) #generating encryption key

def encrypt(message): #encryption function
    try:
        nonce = secrets.token_bytes(12) #unique nonce for each message (12-bytes)
        aes = AESGCM(key) #encrpytion key
        ciphertext = aes.encrypt(nonce, message.encode(), None) #encrypts plain text message into cipher text using key and nonce
        return nonce + ciphertext #returns cipher text packaged with nonce
    except Exception as e:
        raise CryptoError(f"Encryption failed: {e}") #catch errors encrypting


def decrypt(data): #decryption function
    try:
        nonce = data[:12] #nonce makes up first 12 bytes of data
        ciphertext = data[12:]  #remainding data is cipher text
        aes = AESGCM(key) #encrpytion key
        plaintext = aes.decrypt(nonce, ciphertext, None) #decrypts cipher text into pain text using key and nonce
        return plaintext.decode() #returns plain text
    except Exception as e:
        raise CryptoError(f"Decryption failed: {e}") #catch errors decrypting
