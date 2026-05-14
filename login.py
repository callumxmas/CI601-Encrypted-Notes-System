from os import urandom
import hashlib
from AES_256 import deriveKey
from error import *
from pathlib import Path
import tkinter as tk
import tkinter.font as tkFont

def center_window(window): #places window in the middle of the users screen
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def hashPass(password): #password hash function
    return hashlib.sha256(password.encode()).hexdigest() #returns hash of inputted value

def loginWindow(openMenu): #open login window function
    loginWin = tk.Tk() #creates window
    loginWin.title("Login") #window title
    loginWin.geometry("500x400") #window size
    center_window(loginWin) #centers log in window
    loginWin.resizable(False, False) #disables ability to resize window
    loginWin.attributes("-fullscreen", False) #disables ability to full screen window

    titleFont = tkFont.Font(family="Helvetica", size=90, weight="bold") #title font
    subTitleFont = tkFont.Font(family="Helvetica", size=20, weight="bold") #sub title font
    labelFont = tkFont.Font(family="Helvetica", size=10) #lable font

    usernameEntry = tk.Entry(loginWin, width=25, bg="#2b2b2b", fg="white") #sets username input box
    usernameEntry.place(relx=0.5, rely=0.63, anchor="center") #places input box

    passwordEntry = tk.Entry(loginWin, width=25,bg="#2b2b2b", fg="white", show="*") #sets password input box
    passwordEntry.place(relx=0.5, rely=0.75, anchor="center") #places input box

    loginButton = tk.Button(loginWin, text="Login", command=lambda: attemptLogin()) #set login button to login function
    loginButton.place(relx=0.5, rely=0.87, anchor="center") #places button

    createUserLable = tk.Label(loginWin, text="New user?", font=labelFont, fg="grey", bg=loginWin["bg"]) #sets new user label
    createUserLable.place(relx=0.5, rely=0.94, anchor="center") #places label
    createUserLable.bind("<Button-1>", lambda e, lbl=createUserLable, name="createUser": createUser(loginWin, openMenu)) #link create user function

    titleLabel = tk.Label(loginWin,text="N🔒TES",font=titleFont,fg="white",bg=loginWin["bg"]) #sets title label
    titleLabel.place(relx=0.5, rely=0.30, anchor="center") #places label

    subTitleLabel = tk.Label(loginWin, text="AES 256 Encryption", font=subTitleFont, fg="white", bg=loginWin["bg"]) #sets sub title label
    subTitleLabel.place(relx=0.5, rely=0.45, anchor="center") #places label

    userLabel = tk.Label(loginWin, text="Username", font=labelFont, fg="grey", bg=loginWin["bg"]) #sets username label
    userLabel.place(relx=0.5, rely=0.57, anchor="center") #places label

    passLabel = tk.Label(loginWin, text="Password", font=labelFont, fg="grey", bg=loginWin["bg"]) #sets password label
    passLabel.place(relx=0.5, rely=0.69, anchor="center") #places label

    errorLabel = tk.Label(loginWin, text="", font=labelFont, fg="red", bg=loginWin["bg"]) #sets error label
    errorLabel.place(relx=0.5, rely=0.81, anchor="center") #places label

    def attemptLogin(): #attempt login function
        username = usernameEntry.get() #fetch username from input box
        password = passwordEntry.get() #fetch password from input box

        try:
            attempt = login(username, password) #attempt login
            if attempt == True: #if log in success
                with open(f"./users/{username}/credentials/salt.bin", "rb") as f: #read users salt file
                    salt = f.read() #set users salt

                key = deriveKey(str(hashPass(password)), salt) #derive users key using password hash and salt
                loginWin.destroy() #close log in window
                openMenu(username, key) #open menu window passing username and derived key
            else:
                errorLabel.config(text=attempt) #if login fail, display reason
        except AuthError as e:
            errorLabel.config(text=f"Login Error: {str(e)}") #if login error, display error

    def devSkip(): #developer login skip
        with open(f"./users/dev/credentials/salt.bin", "rb") as f: #read dev salt file
            salt = f.read() #set dev salt
        key = deriveKey(str(hashPass("password1!")), salt) #derive dev key using password hash and salt
        loginWin.destroy() #close log in window
        openMenu("dev", key) #open menu window passing in dev credentials

    loginWin.bind_all('<Return>', lambda event: attemptLogin()) #bind enter/return to login function
    loginWin.bind_all('<Control_L>', lambda event: devSkip()) #bind left control key to dev login skip

    loginWin.mainloop() #set login window as main loop

def checkUsername(username): #function to check if username match
    currentUsernames = [d.name for d in Path("./users").iterdir() if d.is_dir()]  #gets list of user directories (users)
    if username not in currentUsernames: #if no match found
        return False #return false
    else: #username found
        return True  #return true

def login(usernameInput, passwordInput): #login function
    if not checkUsername(usernameInput): #check inputted username
        return "Invalid Username" #return error

    try:
        password = safeRead(f"./users/{usernameInput}/credentials/credentials.txt") #attempt to read stored password
    except FileReadError as e:
        return f"Error Reading Credentials: {e}" #returns error if fail

    if str(hashPass(passwordInput)) == password: #checks if inputted hash password matches stored hash
        return True #return true if match
    else:
        return "Invalid Password" #invalid password prompt if password hashes don't match

def createUser(loginWin, openMenu): #open create new user window function
    loginWin.destroy() #close login window

    createUserWin = tk.Tk() #creates window
    createUserWin.title("N🔒TES") #window title
    createUserWin.geometry("500x400") #window size
    center_window(createUserWin) #centers create window

    createUserWin.resizable(False, False) #disables ability to resize window
    createUserWin.attributes("-fullscreen", False) #disables ability to full screen window

    hidePass = True #set password input to be hidden
    hideRepass = True #set password re-enter input to be hidden

    subTitleFont = tkFont.Font(family="Helvetica", size=20, weight="bold") #sub title font
    labelFont = tkFont.Font(family="Helvetica", size=12) #label font
    textFont = tkFont.Font(family="Helvetica", size=10) #sub label font

    subTitleLabel = tk.Label(createUserWin, text="Create a new user!", font=subTitleFont, fg="white") #set create user message label
    subTitleLabel.place(relx=0.5, rely=0.1, anchor="center") #place label

    usernameEntry = tk.Entry(createUserWin, width=25, bg="#2b2b2b", fg="white") #sets username input box
    usernameEntry.place(relx=0.5, rely=0.3, anchor="center") #places input box

    passwordEntry = tk.Entry(createUserWin, width=25, bg="#2b2b2b", fg="white", show="*") #sets password input box
    passwordEntry.place(relx=0.5, rely=0.50, anchor="center") #places input box

    passwordReentry = tk.Entry(createUserWin, width=25, bg="#2b2b2b", fg="white", show="*") #sets password re-entry input box
    passwordReentry.place(relx=0.5, rely=0.80, anchor="center") #places input box

    backButton = tk.Button(createUserWin, text="Back", command=lambda: back(openMenu)) #sets back button to back function
    backButton.place(relx=0.1, rely=0.90, anchor="center") #places button

    createButton = tk.Button(createUserWin, text="Create!", command=lambda: attemptCreateUser()) #sets create button to create user function
    createButton.place(relx=0.9, rely=0.90, anchor="center") #places button

    userLabel = tk.Label(createUserWin, text="Username", font=labelFont, fg="white") #sets username label
    userLabel.place(relx=0.5, rely=0.24, anchor="center") #places label

    userText = tk.Label(createUserWin, text="Usernames are case sensitive and should not include spaces.", font=textFont, fg="grey") #sets username rules label
    userText.place(relx=0.5, rely=0.36, anchor="center") #places label

    passLabel = tk.Label(createUserWin, text="Password", font=labelFont, fg="white") #sets password label
    passLabel.place(relx=0.5, rely=0.43, anchor="center") #places label

    passText = tk.Label(createUserWin, text="Passwords should adhere to the following standards: ", font=textFont, fg="grey") #sets password rules label
    passText.place(relx=0.5, rely=0.56, anchor="center") #places label

    rule1text = tk.Label(createUserWin, text="- Minimum 8 characters", font=textFont,fg="grey") #sets password rule 1 label
    rule1text.place(relx=0.25, rely=0.59) #places label

    rule2text = tk.Label(createUserWin, text="- Contain a number", font=textFont, fg="grey") #sets password rule 2 label
    rule2text.place(relx=0.25, rely=0.63) #places label

    rule3text = tk.Label(createUserWin, text="- Contain a special character", font=textFont, fg="grey") #sets password rule 3 label
    rule3text.place(relx=0.25, rely=0.67) #places label

    repassLabel = tk.Label(createUserWin, text="Re-enter password", font=labelFont, fg="white") #sets password re-entry label
    repassLabel.place(relx=0.5, rely=0.74, anchor="center") #places label

    errorLabel = tk.Label(createUserWin, text="", font=textFont, fg="red") #sets error label
    errorLabel.place(relx=0.5, rely=0.86, anchor="center") #places label

    showPassButton = tk.Label(createUserWin, text="🙈", font=labelFont) #sets show password label
    showPassButton.place(relx=0.77, rely=0.5, anchor="center") #places lable
    showPassButton.bind("<Button-1>",lambda e, lbl=showPassButton, name="showPass": showPass()) #binds show password function to label press
    showPassButton.bind("<ButtonRelease-1>", lambda e, lbl=showPassButton, name="hidePass": hidePass()) #binds hide password function to label release

    showRepassButton = tk.Label(createUserWin, text="🙈", font=labelFont) #sets show password re-entry label
    showRepassButton.place(relx=0.77, rely=0.8, anchor="center") #places lable
    showRepassButton.bind("<Button-1>",lambda e, lbl=showRepassButton, name="showRepass": showRepass()) #binds show password re-entry function to label press
    showRepassButton.bind("<ButtonRelease-1>", lambda e, lbl=showRepassButton, name="hideRepass": hideRepass()) #binds hide password re-entry function to label release

    def back(openMenu): #back function
        createUserWin.destroy() #closes create user window
        loginWindow(openMenu) #opens login window

    def showPass(): #show password function
        showPassButton.config(text="🙉") #set password monkey to see
        passwordEntry.config(show="") #set password to plaintext

    def hidePass(): #hide password function
        showPassButton.config(text="🙈") #set password monkey to not see
        passwordEntry.config(show="*") #set password to *

    def showRepass(): #show password re-entry function
        showRepassButton.config(text="🙉") #set password re-entry monkey to see
        passwordReentry.config(show="") #set password re-entry to plaintext

    def hideRepass(): #hide password re-entry function
        showRepassButton.config(text="🙈") #set password re-entry monkey to not see
        passwordReentry.config(show="*") #set password re-entry to *

    def attemptCreateUser(): #attempt create new user function
        userText.config(fg="grey") #reset label colours and error label
        passText.config(fg="grey")
        errorLabel.config(text="")
        rule1text.config(fg="grey")
        rule2text.config(fg="grey")
        rule3text.config(fg="grey")

        inputtedUsername = usernameEntry.get() #fetch username
        inputtedPassword = passwordEntry.get() #fetch password
        inputtedRePassword = passwordReentry.get() #fetch password re-entry

        if inputtedUsername == "": #if username is empty
            errorLabel.config(text="Enter a username") #display error
            return #skip

        elif len(inputtedUsername) > 40: #if username is longer than 40 chars
            errorLabel.config(text="Username too long (max 40 characters)") #display error
            return #skip

        elif checkUsername(inputtedUsername): #if username is taken
            errorLabel.config(text="Username already taken") #display error
            return #skip

        elif inputtedUsername.find(" ") >= 1: #if username contains a space
            userText.config(fg="red") #highlight username rules in red
            return #skip

        elif inputtedPassword == "": #if password is empty
            errorLabel.config(text="Enter a password") #display error
            return #skip

        elif len(inputtedPassword) < 8: #if password is shorter than 8 chars
            rule1text.config(fg="red") #highlight password rule 1 in red
            return #skip

        elif not any(c.isdigit() for c in inputtedPassword): #if password does not contain a number
            rule2text.config(fg="red") #highlight password rule 2 in red
            return #skip

        elif not any(not c.isalnum() for c in inputtedPassword): #if password does not contain a special char
            rule3text.config(fg="red") #highlight password rule 3 in red
            return #skip

        elif inputtedPassword != inputtedRePassword: #if password and password re-entry do not match
            errorLabel.config(text="Passwords do not match") #display error
            return #skip

        else: #if all rules are met
            makeNewUser(inputtedUsername, inputtedPassword) #pass username and password into make new user function

    def makeNewUser(username, password): #make new user function
        hashedP = str(hashPass(password)) #hash inputted password

        Path(f"./users/{username}").mkdir(parents=True, exist_ok=True) #make user directory
        Path(f"./users/{username}/credentials").mkdir(parents=True, exist_ok=True) #make user's credential directory
        Path(f"./users/{username}/bin").mkdir(parents=True, exist_ok=True) #make user's bin
        safeWrite(f"./users/{username}/credentials/credentials.txt", hashedP) #store user's hashed password

        salt = urandom(16) #generate user's unique salt
        with open(f"./users/{username}/credentials/salt.bin", "wb") as f: #open user's salt file
            f.write(salt) #store user's salt

        key = deriveKey(hashedP, salt) #derive user's key using hashed password and salt
        createUserWin.destroy() #close new user window
        openMenu(username, key) #open menu window passing in username and derived key

    createUserWin.bind_all('<Return>', lambda event: attemptCreateUser()) #bind enter/return to create user function
    createUserWin.mainloop() #set create new user function as main loop