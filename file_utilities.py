import AES_256
from error import *

def loadFile(username,filename): #load file function
    try:
        hexdata = safeRead(f"./{username}/{filename}") #attempt to read stored hexadecimal data from inputted file

        if not hexdata: #if file hexdata is empty
            raise FileReadError("File is empty") #raise file empty error

        try:
            data = bytes.fromhex(hexdata) #casts hex data to bytes
        except ValueError:
            raise FileReadError("File corrupt") #raise file corrupt error if fail

        try:
            plaintext = AES_256.decrypt(data) #attempt to decrypt byte data to plain text
        except CryptoError as e:
            raise CryptoError(f"Decryption Error: {e}") #raise decryption error if fail

        print("Decrypted:", plaintext)
        return  plaintext #return decrypted plain text

    except (FileReadError, CryptoError):
        raise #raise error is load fails

def writeFile(path, data): #write to file function
    try:
        ciphertext = AES_256.encrypt(data).hex() #encrypts inputted data
        print(f"Encrypted: {ciphertext} to {path}")
        safeWrite(path, ciphertext) #writes to file
    except (FileWriteError, CryptoError) as e:
        raise FileWriteError(f"File Write Error: {e}") #raises error if fail

def createFile(username, filename): #create file function
    try:
        safeWrite(f"./{username}/{filename}.txt", AES_256.encrypt("").hex()) #attempt to write to new file
    except FileWriteError as e:
        raise FileWriteError(f"File Create Error: {e}") #raises error if fail

def moveFile(oldFile, newFile): #move file function
    try:
        safeMove(oldFile, newFile) #attempt to move file location
    except FileWriteError as e:
        raise FileWriteError (f"File Move Error: {e}") #raises error if fail

def deleteFile(path): #delete file function
    try:
        safeDelete(path) #attempt to delete file
    except DeleteFileError as e:
        raise DeleteFileError(f"File Delete Error: {e}") #raises error if fail

def renameFile(path,renamePath): #rename file function
    try:
        safeRename(path, renamePath) #attempt to rename file
    except FileWriteError as e:
        raise FileWriteError(f"File Rename Error: {e}") #displays error if fail