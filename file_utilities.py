import AES_256
from error import *

def loadFile(username,filename): #load file function
    try:
        hexdata = safeRead(f"./{username}/{filename}") #attempt to read stored hexadecimal data from inputted file

        if not hexdata: #if file hexdata is empty
            raise FileReadError("File is empty") #raise file empty error

        data = bytes.fromhex(hexdata) #cast hex data to bytes
        plaintext = AES_256.decrypt(data) #decrypts byte data to plain text

        print("Decrypted:", plaintext)
        return  plaintext #return decrypted plain text

    except FileReadError as e:
        return "Read Error:", e #catches error reading file
    except ValueError:
        return"File does not contain valid hex" #catches errors reading hex data

    except CryptoError as e:
        return"Decryption Error:", e #catches errors decrypting data

def writeFile(path, data): #write to file function
    ciphertext = AES_256.encrypt(data).hex() #encrypts inputted data
    print(f"Encrypted: {ciphertext} to {path}")
    safeWrite(path, ciphertext) #writes to file