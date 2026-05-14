import file_utilities
from login import loginWindow
from pathlib import Path
import tkinter as tk
import tkinter.font as tkFont

def openMenuWin(username): #opens main menu window function
    root = tk.Tk() #creates window
    root.title("N🔒TES") #window title
    root.geometry("1000x500") #window size

    currentFileLable = None #lable currently selected
    currentFileName = None #filename currently selected

    fileExplore = tk.Canvas(root,width=220,height=406,bg="#2b2b2b") #set file explore canvas
    fileExplore.place(x=20, y=20) #place file explorer

    scrollbar = tk.Scrollbar(root, orient="vertical", command=fileExplore.yview) #sets scrollbar
    scrollbar.place(x=24 + 220, y=23, height=406) #places scrollbar
    fileExplore.configure(yscrollcommand=scrollbar.set) #links file explore with scroll bar

    fileList = tk.Frame(fileExplore, bg="#2b2b2b", padx=5, pady=5) #set file list frame
    fileExplore.create_window((0, 0), window=fileList, anchor="nw") #sets file explorer window
    def update_scroll(event): #update scroll function
        fileExplore.configure(scrollregion=fileExplore.bbox('all')) #scroll affects all files displayed
    fileList.bind("<Configure>", update_scroll) #bind to file list

    topBlock = tk.Canvas(root, width=220, height=10, bg="#1E1E1E", borderwidth=0) #sets file explorer top border
    topBlock.place(x=20, y=7) #places border

    bottomBlock = tk.Canvas(root, width=220, height=10, bg="#1E1E1E") #sets file explorer bottom border
    bottomBlock.place(x=20, y=429) #places border

    editorFrame = tk.Frame(root, width=700,height=406, bg="#2b2b2b") #sets file editor frame
    editorFrame.place(x=280, y=23) #places frame

    fileEditor = tk.Text(editorFrame, font=("Helvetica", 16), bg= "#2b2b2b", width=77,height=21) #sets file text editor
    notifyLable = tk.Label(editorFrame, text="", fg="grey", bg="#2b2b2b") #sets notification lable

    createFileButton = tk.Button(root, text="New File", command=lambda: newFilePopUp()) #sets new file button
    createFileButton.place(x=20, y=445) #places button

    deleteFileButton = tk.Button(root, text="Delete", command=lambda: deletePopUp()) #sets delete file button
    deleteFileButton.place(x=106, y=445) #places button

    renameFileButton = tk.Button(root, text="Rename", command=lambda: renamePopUp()) #sets rename file button
    renameFileButton.place(x=180, y=445) #places button

    saveFileButton = tk.Button(root, text="Save", command=lambda: saveFile()) #sets save file button
    saveFileButton.place(x=280, y=445) #places button

    logoutFileButton = tk.Button(root, text="Log Out", command=lambda: logout()) #sets logout button
    logoutFileButton.place(x=897, y=445) #places button

    filesLable = tk.Label(root, text="Files:", fg="grey") #sets files lable
    filesLable.place(x=20, y=0) #places lable

    fileTitle = tk.Label(root, text="", fg="grey") #sets opened files title
    fileTitle.place(x=280, y=0) #places lable

    fileFont = tkFont.Font(family="Helvetica", size=15, weight="bold") #file list font

    def logout(): #logout function
        root.destroy() #closes menu window
        loginWindow(openMenuWin) #opens login window

    def loadFiles(): #function to loads user's files
        files = [f for f in Path("./" + username).glob("*.txt")if f.name != "credentials.txt"] #loops though user's directory looking for .txt files (except credentials.txt)
        return files #returns file list

    def openFile(lable, filename): #open file function
        nonlocal currentFileName, currentFileLable

        print(f"Opening: {filename}")
        currentFileLable = lable #sets selected lable
        currentFileName = filename #sets selected filename

        fileTitle.config(text=currentFileName) #sets filename title
        lable.config(text="🔓 " + currentFileName[:-4], fg="grey") #sets lable to display as open

        fileEditor.place(x=0, y=0) #places file editor title
        data = file_utilities.loadFile(username, filename) #loads data from file
        fileEditor.insert(tk.END, data) #places data in editor

    def closeFile(): #close file function
        nonlocal currentFileName, currentFileLable

        print(f"Closing: {currentFileName}")

        fileTitle.config(text="") #clears filename title
        currentFileLable.config(text="🔒 " + currentFileName[:-4], fg="white") #sets lable to display as closed

        fileEditor.delete("0.0", "end") #clears editor
        fileEditor.place_forget() #closes editor

    def fileClick(lable): #file click function
        nonlocal currentFileName, currentFileLable

        notifyLable.config(text="") #clears center lable
        filename = lable.cget("text")[2:]+".txt" #sets filename by removing lock symbol & adding file extension

        if currentFileLable == None: #checks if no file is currently open
            openFile(lable,filename) #if so opens
            return #skip
        elif filename != currentFileName: #checks if new file is opening
            closeFile() #closes current file
            openFile(lable,filename) #opens new file
            return #skip
        elif currentFileLable == lable: #checks if file open is the same as file being clicked
            return #skip

    def displayFiles(): #display/update file list function
        files = loadFiles() #loads files
        print(len(files))

        for widget in fileList.winfo_children(): #loops through current file list
            widget.destroy() #clears each lable

        for f in files: #loop through each file
            filename = f.name #sets file name
            fileLabel = tk.Label(fileList,text="🔒 "+filename[:-4],font=fileFont,fg="white",bg="#2b2b2b",pady=13,anchor="w",width=20,) #sets lable
            fileLabel.pack(fill="x", padx=10) #places lable

            border = tk.Frame(fileList, bg="#444444", height=1) #creates line divider
            border.pack(fill="x", padx=5) #places divider

            fileLabel.bind("<Button-1>", lambda e, lbl=fileLabel, name=filename: fileClick(lbl)) #sets file lable as clickable

        if len(files) == 0:  # if no files are found
            notifyLable.place(relx=0.5, rely=0.5, anchor="center")  # places center lable
            notifyLable.config(text="No Files! Select 'New File'.")  # displays no files found
            return
        elif len(files) != 0 and currentFileName is None:  # if files found but none selected
            notifyLable.place(relx=0.5, rely=0.5, anchor="center")  # places center lable
            notifyLable.config(text="Select a File!")  # displays no file selected

    def saveFile(): #save file function
        if currentFileLable is not None: #checks a file is currently open
            print("SAVING!")
            dataToSave = fileEditor.get("1.0", "end") #reads text editor
            print(dataToSave)
            file_utilities.writeFile(f"./{username}/{currentFileName}",dataToSave) #saves to file

    def deletePopUp(): #delete file pop up window
        nonlocal currentFileName
        if currentFileName is None: #checks a file is currently open
            return #skips if not

        PopUp = tk.Toplevel(root) #creates window
        PopUp.title("File Delete") #window title
        PopUp.geometry("400x130") #window size

        labelFont = tkFont.Font(family="Helvetica", size=14)  #lable font
        titleFont = tkFont.Font(family="Helvetica", size=16, weight="bold")  #title font

        popUpTitleLabel = tk.Label(PopUp, text=f"Confirm deleting {currentFileName}?", font=titleFont,fg="white") #delete message
        popUpTitleLabel.place(relx=0.5, rely=0.20, anchor="center") #places lable

        popUpLable = tk.Label(PopUp, text="Once a file is deleted, it is unrecoverable.", font=labelFont,fg="grey") #delete sub message
        popUpLable.place(relx=0.5, rely=0.50, anchor="center") #places lable

        cancelButton = tk.Button(PopUp, text="Cancel",command=lambda: PopUp.destroy()) #sets cancel button to close window
        cancelButton.place(relx=0.35, rely=0.80, anchor="center") #places button

        deleteButton = tk.Button(PopUp, text="Delete")  #sets delete button
        deleteButton.place(relx=0.65, rely=0.80, anchor="center")  #places button

    def renamePopUp(): #rename file pop up window
        nonlocal currentFileLable, currentFileName

        if currentFileName is None: #if no file is selected
            return #skip

        PopUp = tk.Toplevel(root) #creates window
        PopUp.title("File Rename") #window title
        PopUp.geometry("400x130") #window size

        labelFont = tkFont.Font(family="Helvetica", size=14)  #lable font

        popUpLabel = tk.Label(PopUp, text=f"Rename {currentFileName[:-4]}", font=labelFont, fg="white") #rename message
        popUpLabel.place(relx=0.5, rely=0.20, anchor="center") #place lable

        fileNameInput = tk.Entry(PopUp, width=25, bg="#2b2b2b", fg="white") #name input bpx
        fileNameInput.place(relx=0.5, rely=0.40, anchor="center") #place input box
        fileNameInput.insert(0, currentFileName[:-4]) #put current file name in input box (without extension)

        renameButton = tk.Button(PopUp, text="Rename") #set rename button
        renameButton.place(relx=0.65, rely=0.80, anchor="center") #place rename button

        cancelButton = tk.Button(PopUp, text="Cancel", command=lambda: PopUp.destroy()) #set cancel button to close window
        cancelButton.place(relx=0.35, rely=0.80, anchor="center") #place cancel button

        errorLabel = tk.Label(PopUp, text="", font=labelFont, fg="red") #sets error lable
        errorLabel.place(relx=0.5, rely=0.60, anchor="center") #places lable

    def newFilePopUp(): #new file pop up window
        PopUp = tk.Toplevel(root) #creates window
        PopUp.title("New File") #window title
        PopUp.geometry("400x130") #window size

        labelFont = tkFont.Font(family="Helvetica", size=14) #lable font

        popUpLabel = tk.Label(PopUp, text="New File Name", font=labelFont, fg="white") #sets new file message
        popUpLabel.place(relx=0.5, rely=0.20, anchor="center") #places label

        fileNameInput = tk.Entry(PopUp,width=25, bg="#2b2b2b", fg="white") #sets filename input box
        fileNameInput.place(relx=0.5, rely=0.40, anchor="center") #places input box

        createButton = tk.Button(PopUp, text="Create") #sets create button
        createButton.place(relx=0.65, rely=0.80, anchor="center") #places button

        cancelButton = tk.Button(PopUp, text="Cancel", command=lambda: PopUp.destroy()) #sets cancel button to close window
        cancelButton.place(relx=0.35, rely=0.80, anchor="center") #places button

        errorLabel = tk.Label(PopUp, text="", font=labelFont, fg="red") #sets error lable
        errorLabel.place(relx=0.5, rely=0.60, anchor="center") #places error lable

    displayFiles() #updates file list

    root.mainloop() #set main menu (root) as main loop

loginWindow(openMenuWin) #calls login function to start the program