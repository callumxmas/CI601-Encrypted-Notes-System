import AES_256
from error import *
from pathlib import Path

def writefile(filename): #write to file function
    message = input("Enter message: ") #text input

    try:
        ciphertext = AES_256.encrypt(message).hex() #main encryption method call
        safe_write(filename, ciphertext) #write cipher text to file
        print("Encrypted: ", ciphertext) #print cipher text

    except FileWriteError as e:
        print("Write Error:", e) #catch errors with writing to file

    except CryptoError as e:
        print("Encryption Error:", e) #catch errors with encryption


def readfile(filename): #read from file function
    try:
        hexdata = safe_read(filename) #reads stored hexadecimal data from file

        if not hexdata:
            raise FileReadError("File is empty") #checks if file is empty

        data = bytes.fromhex(hexdata) #casting hex data to bytes
        plaintext = AES_256.decrypt(data) #decrypts byte data to plain text

        print("Decrypted:", plaintext) #prints plaintext

    except FileReadError as e:
        print("Read Error:", e) #catch errors reading file

    except ValueError:
        print("File does not contain valid hex") #catch errors reading hex data

    except CryptoError as e:
        print("Decryption Error:", e) #catch errors decrypting data

def login(): #login function
    while True:
        username = input("Username: ") #input username
        usernames = [d.name for d in Path(".").iterdir() if d.is_dir()] #gets list of user directories (users)
        if username not in usernames: #checks if inputted user is valid
            print ("Invalid Username") #invalid username prompt
            continue #restarts login due to invalid username

        passwordInput = input("Password: ") #input password

        try:
            password = safe_read(f"./{username}/credentials.txt") #reads stored password
        except FileReadError as e:
            print("Error reading credentials:", e) #catch errors reading password
            continue #restarts login

        if passwordInput == password: #checks if password matches
            print("<-login success->") #success prompt
            menu(username) #calls menu function
        else:
            print("Invalid Password") #invalid password prompt
            #restarts login due to invalid password

def menu(username): #menu function
    while True:
        files = [f for f in Path("./" + username).glob("*.txt") #lists text(.txt) files within user's directory
                     if f.name != "credentials.txt"] #excludes credentials file from list
        files.sort() #sorts list

        print("Files:")
        for index, FILES in enumerate(files, start=1): #loops through list
            print(index ,"-> ", FILES.name[:-4]) #prints each file name (excluding file extension)

        try:
            file = f"./{files[int(input(""))-1]}" #file path is assigned from user input
        except:
            print("Invalid File") #invalid file prompt
            continue #restarts file selection

        mode = input("Select Mode [write(w) read(r) re-select(s)]: ") #prompts user to select mode
        if mode == "w": #w to write to selected file
            writefile(file) #function call
        elif mode == "r": #r to read selected file
            readfile(file) #function call
        elif mode == "s": #s to re-select file
            continue #restarts file selection
        else:
            print("Invalid Mode") #invalid mode prompt

login() #calls login function to start the program