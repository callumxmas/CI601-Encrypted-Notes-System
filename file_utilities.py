import AES_256
from error import *

def loadFile(username,filename,key): #load file function
    try:
        hexdata = safeRead(f"./users/{username}/{filename}") #attempt to read stored hexadecimal data from inputted file

        if not hexdata: #if file hexdata is empty
            raise FileReadError("File is empty") #raise file empty error

        try:
            data = bytes.fromhex(hexdata) #attempt to cast hex data to bytes
        except ValueError:
            raise FileReadError("File corrupt") #raise file corrupt error if fail

        try:
            plaintext = AES_256.decrypt(data,key) #attempt to decrypt byte data to plain text
        except CryptoError as e:
            raise CryptoError(f"Decryption Error: {e}") #raise decryption error if fail

        return  plaintext #return decrypted plain text

    except (FileReadError, CryptoError):
        raise #raise error is load fails

def writeFile(path, data, key): #write to file function
    try:
        ciphertext = AES_256.encrypt(data, key).hex() #attempt to encrypt inputted data using inputted key
        safeWrite(path, ciphertext) #write ciphertext to file
    except (FileWriteError, CryptoError) as e:
        raise FileWriteError(f"File Write Error: {e}") #raise error if fail

def createFile(username, filename,key): #create file function
    try:
        safeWrite(f"./users/{username}/{filename}.txt", AES_256.encrypt("",key).hex()) #attempt to write to new file
    except FileWriteError as e:
        raise FileWriteError(f"File Create Error: {e}") #raise error if fail

def moveFile(oldFile, newFile): #move file function
    try:
        safeMove(oldFile, newFile) #attempt to move file location
    except FileWriteError as e:
        raise FileWriteError (f"File Move Error: {e}") #raise error if fail

def deleteFile(path): #delete file function
    try:
        safeDelete(path) #attempt to delete file
    except DeleteFileError as e:
        raise DeleteFileError(f"File Delete Error: {e}") #raise error if fail

def renameFile(path,renamePath): #rename file function
    try:
        safeRename(path, renamePath) #attempt to rename file
    except FileWriteError as e:
        raise FileWriteError(f"File Rename Error: {e}") #displays error if fail