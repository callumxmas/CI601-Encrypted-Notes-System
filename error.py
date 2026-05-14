from pathlib import Path

class FileReadError(Exception):#file cannot be read
    pass

class FileWriteError(Exception):#file cannot be written
    pass

class AuthError(Exception):#login authentication fail
    pass

class CryptoError(Exception):#encryption or decryption fail
    pass

def safeRead(path): #file reading function producing specific errors
    try:
        return Path(path).read_text() #read attempt
    except FileNotFoundError:
        raise FileReadError(f"File not found: {path}")
    except PermissionError:
        raise FileReadError(f"Permission denied: {path}")
    except Exception as e:
        raise FileReadError(f"Error reading file {path}: {e}")

def safeWrite(path, data): #file writing function producing specific errors
    try:
        Path(path).write_text(data) #write attempt
    except PermissionError:
        raise FileWriteError(f"Permission denied: {path}")
    except Exception as e:
        raise FileWriteError(f"Error writing to file {path}: {e}")