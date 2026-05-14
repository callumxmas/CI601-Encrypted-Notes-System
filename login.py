from error import *
from pathlib import Path
import tkinter as tk
import tkinter.font as tkFont

def loginWindow(openMenu): #open login window function
    loginWin = tk.Tk() #creates window
    loginWin.title("Login") #window title
    loginWin.geometry("500x400") #window size

    titleFont = tkFont.Font(family="Helvetica", size=90, weight="bold") #title font
    subTitleFont = tkFont.Font(family="Helvetica", size=20, weight="bold") #sub title font
    labelFont = tkFont.Font(family="Helvetica", size=10) #lable font

    usernameEntry = tk.Entry(loginWin, width=25, bg="#2b2b2b", fg="white") #sets username input box
    usernameEntry.place(relx=0.5, rely=0.63, anchor="center") #places input box

    passwordEntry = tk.Entry(loginWin, width=25,bg="#2b2b2b", fg="white", show="*") #sets password input box
    passwordEntry.place(relx=0.5, rely=0.75, anchor="center") #places input box

    loginButton = tk.Button(loginWin, text="Login", command=lambda: attemptLogin()) #set login button
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
        print("Attempting login...")
        username = usernameEntry.get() #fetch username from input box
        password = passwordEntry.get() #fetch password from input box

        try:
            attempt = login(username, password) #attempt login
            if attempt == True: #if log in success
                print("loging in...")
                loginWin.destroy() #close log in window
                openMenu(username) #open menu window passing in username
            else:
                errorLabel.config(text=attempt) #if login fail, display reason
        except AuthError as e:
            print("Login Error", str(e)) #if login error, print error

    loginWin.mainloop() #set login window as main loop

def checkUsername(username): #function to check if username match
    currentUsernames = [d.name for d in Path(".").iterdir() if d.is_dir()] #gets list of user directories (users)
    if username not in currentUsernames: #if no match found
        return False #return false
    else: #username found
        return True  #return true

def login(usernameInput, passwordInput): #login function
    if not checkUsername(usernameInput): #check inputted username
        return "Invalid Username" #return error no match found

    try:
        password = safeRead(f"./{usernameInput}/credentials.txt") #attempt to read stored password
    except FileReadError as e:
        print("Error reading credentials:", e)
        return "Error reading credentials" #displays error if fail

    if passwordInput == password: #checks if password matches
        print("<-login success->")
        return True #return true if match
    else:
        return "Invalid Password" #invalid password prompt if doesn't match

def createUser(loginWin, OpenMenu): #open create new user window function
    loginWin.destroy() #close login window

    createUserWin = tk.Tk()  #creates window
    createUserWin.title("N🔒TES")  #window title
    createUserWin.geometry("500x400")  #window size

    subTitleFont = tkFont.Font(family="Helvetica", size=20, weight="bold") #sub title font
    labelFont = tkFont.Font(family="Helvetica", size=12) #label font
    textFont = tkFont.Font(family="Helvetica", size=10) #sub label font

    sub_title_label = tk.Label(createUserWin, text="Create a new user!", font=subTitleFont, fg="white") #set create user message label
    sub_title_label.place(relx=0.5, rely=0.1, anchor="center") #place label

    username_entry = tk.Entry(createUserWin, width=25, bg="#2b2b2b", fg="white") #sets username input box
    username_entry.place(relx=0.5, rely=0.3, anchor="center") #places input box

    password_entry = tk.Entry(createUserWin, width=25, bg="#2b2b2b", fg="white", show="*") #sets password input box
    password_entry.place(relx=0.5, rely=0.50, anchor="center") #places input box

    password_reentry = tk.Entry(createUserWin, width=25, bg="#2b2b2b", fg="white", show="*") #sets password re-entry input box
    password_reentry.place(relx=0.5, rely=0.80, anchor="center") #places input box

    back_button = tk.Button(createUserWin, text="Back", command=lambda: back(OpenMenu)) #sets back button to back function
    back_button.place(relx=0.1, rely=0.90, anchor="center") #place button

    create_button = tk.Button(createUserWin, text="Create!") #sets create button
    create_button.place(relx=0.9, rely=0.90, anchor="center") #place button

    user_label = tk.Label(createUserWin, text="Username", font=labelFont, fg="white") #sets username label
    user_label.place(relx=0.5, rely=0.24, anchor="center") #place label

    user_text = tk.Label(createUserWin, text="Usernames are case sensitive and should not include spaces.", font=textFont, fg="grey") #sets username rules label
    user_text.place(relx=0.5, rely=0.36, anchor="center") #place label

    pass_label = tk.Label(createUserWin, text="Password", font=labelFont, fg="white") #sets password label
    pass_label.place(relx=0.5, rely=0.43, anchor="center") #place label

    pass_text = tk.Label(createUserWin, text="Passwords should adhere to the following standards: ",font=textFont, fg="grey") #sets password rules label
    pass_text.place(relx=0.5, rely=0.56, anchor="center") #place label

    rule1text = tk.Label(createUserWin, text="- Minimum 8 characters", font=textFont,fg="grey") #sets password rule 1 label
    rule1text.place(relx=0.25, rely=0.59) #place label

    rule2text = tk.Label(createUserWin, text="- Contain a number", font=textFont, fg="grey") #sets password rule 2 label
    rule2text.place(relx=0.25, rely=0.63) #place label

    rule3text = tk.Label(createUserWin, text="- Contain a special character", font=textFont, fg="grey") #sets password rule 3 label
    rule3text.place(relx=0.25, rely=0.67) #place label

    repass_label = tk.Label(createUserWin, text="Re-enter password", font=labelFont, fg="white") #sets password re-entry label
    repass_label.place(relx=0.5, rely=0.74, anchor="center") #place label

    error_label = tk.Label(createUserWin, text="", font=textFont, fg="red") #sets error label
    error_label.place(relx=0.5, rely=0.86, anchor="center") #place label

    def back(OpenMenu): #back function
        createUserWin.destroy() #closes create user window
        loginWindow(OpenMenu) #opens login window

    createUserWin.mainloop() #set create new user function as main loop

