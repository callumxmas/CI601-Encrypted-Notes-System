from error import *
import secrets
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def deriveKey(password,salt): #32-byte key derivation function
    kdf = Scrypt(salt=salt,length=32,n=2**14,r=8,p=1,) #sets Scrypt parameters (using inputted salt)
    return kdf.derive(password.encode("utf-8")) #returns generated key using password and inputted parameters

def encrypt(message, key): #encryption function
    try: #attempts encryption
        nonce = secrets.token_bytes(12) #generates unique nonce for each message (12 bytes)
        aes = AESGCM(key) #set encryption key as key passed in
        ciphertext = aes.encrypt(nonce, message.encode(), None) #encrypts plain text into cipher text using key and nonce
        return nonce + ciphertext #returns cipher text packaged with nonce
    except Exception as e:
        raise CryptoError(f"Encryption failed: {e}") #raises encryption errors

def decrypt(data, key): #decryption function
    try: #attempts decryption
        nonce = data[:12] #fetch nonce from first 12 bytes of data
        ciphertext = data[12:] #remainding data is ciphertext
        aes = AESGCM(key) #set encryption key as key passed in
        plaintext = aes.decrypt(nonce, ciphertext, None) #decrypts cipher text into pain text using key and nonce
        return plaintext.decode() #returns plain text
    except Exception as e:
        raise CryptoError(f"Decryption failed: {e}") #raises decryption errors
