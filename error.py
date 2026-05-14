from pathlib import Path

class FileReadError(Exception):#file cannot be read
    pass

class FileWriteError(Exception):#file cannot be written
    pass

class DeleteFileError(Exception): #file cannot be deleted error
    pass

class AuthError(Exception):#login authentication fail
    pass

class CryptoError(Exception):#encryption or decryption fail
    pass

def safeRead(path): #file reading function (error protected)
    try:
        return Path(path).read_text() #read attempt
    except FileNotFoundError:
        raise FileReadError(f"File not found: {path}") #raise read error
    except PermissionError:
        raise FileReadError(f"Permission denied: {path}") #raise permission error
    except Exception as e:
        raise FileReadError(f"Error reading file {path}: {e}") #raise exception error


def safeWrite(path, data): #file writing function (error protected)
    try:
        Path(path).write_text(data) #write attempt
    except PermissionError:
        raise FileWriteError(f"Permission denied: {path}") #raise write error
    except Exception as e:
        raise FileWriteError(f"Error writing to file {path}: {e}") #raise exception error

def safeDelete(path): #file delete function (error protected)
    try:
        Path(path).unlink() #delete attempt
    except FileNotFoundError:
        raise DeleteFileError(f"File not found: {path}") #raise delete error
    except Exception as e:
        raise DeleteFileError(f"Error deleting file {path}: {e}") #raise exception error

def safeRename(path, rename): #file rename function (error protected)
    try:
        Path(path).rename(Path(rename)) #rename attempt
    except FileNotFoundError:
        raise FileWriteError(f"File not found: {path}") #raise write error
    except Exception as e:
        raise FileWriteError(f"Error renaming file {path}: {e}") #raise exception error

def safeMove(oldPath, newPath): #file move function (error protected)
    try:
        Path(oldPath).rename(Path(newPath)) #rename attempt (move attempt)
    except FileNotFoundError:
        raise FileWriteError(f"File not found: {oldPath}") #raise write error
    except Exception as e:
        raise FileWriteError(f"Error moving file to {newPath}: {e}") #raise exception error