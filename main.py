import datetime
import file_utilities
from error import *
from login import loginWindow
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

def openMenuWin(username, key): #opens main menu window function
    root = tk.Tk() #creates window
    root.title(f"N🔒TES    |    {username}") #window title
    root.geometry("1000x500") #window size
    center_window(root) #centers menu window

    root.resizable(False, False) #disables ability to resize window
    root.attributes("-fullscreen", False) #disables ability to full screen window

    currentFileName = None #no selected file initially
    unsaved = False #unsaved statues is false

    fileExplore = tk.Canvas(root, width=240, height=406,bg="#2b2b2b") #set file explore canvas
    fileExplore.place(x=20, y=20) #place file explorer

    fileList = tk.Frame(fileExplore, bg="#2b2b2b", padx=5, pady=5) #set file list frame
    fileExploreWin = fileExplore.create_window((0, 0), window=fileList, anchor="nw") #sets file explorer window

    def updateScroll(event=None): #update scroll function
        fileExplore.configure(scrollregion=fileExplore.bbox("all")) #scroll affects all files displayed
    fileList.bind("<Configure>", updateScroll) #bind to file list

    def syncWidth(event): #width control function
        fileExplore.itemconfig(fileExploreWin, width=event.width) #configure file explorer width
    fileExplore.bind("<Configure>", syncWidth) #bind to file explore canvas

    fileExplore.configure(yscrollincrement=15) #scroll increment

    def mouseWheel(event): #scroll direction detection function
        if event.delta > 0: #if positive scroll
            fileExplore.yview_scroll(-1, "units") #scroll up
        else: #if negative scroll
            fileExplore.yview_scroll(1, "units") #scroll down

    fileExplore.bind("<Enter>", lambda e: fileExplore.bind_all("<MouseWheel>", mouseWheel)) #binds scrolling to when mouse is on file explorer (mac/windows)
    fileExplore.bind("<Leave>", lambda e: fileExplore.unbind_all("<MouseWheel>")) #unbinds scrolling to when mouse is off file explorer (mac/windows)
    fileExplore.bind_all("<Button-4>", lambda e: fileExplore.yview_scroll(-1, "units")) #linux scroll up
    fileExplore.bind_all("<Button-5>", lambda e: fileExplore.yview_scroll(1, "units")) #linux scroll down

    topBlock = tk.Canvas(root, width=240, height=10, bg="#1E1E1E", borderwidth=0) #sets file explorer top border
    topBlock.place(x=20, y=7) #places border

    bottomBlock = tk.Canvas(root, width=240, height=10, bg="#1E1E1E") #sets file explorer bottom border
    bottomBlock.place(x=20, y=429) #places border

    rsideBlock = tk.Canvas(root, width=10, height=406, bg="#1E1E1E") #sets file explorer right border
    rsideBlock.place(x=260, y=20) #places border

    lsideBlock = tk.Canvas(root, width=10, height=406, bg="#1E1E1E") #sets file explorer left border
    lsideBlock.place(x=10, y=20) #places border

    editorFrame = tk.Frame(root, width=700, height=406, bg="#2b2b2b") #sets file editor frame
    editorFrame.place(x=280, y=23) #places frame

    fileEditor = tk.Text(editorFrame, font=("Helvetica", 16), bg="#2b2b2b", width=77, height=21, undo=True, maxundo=-2) #sets file text editor
    notifyLable = tk.Label(editorFrame, text="", fg="grey", bg="#2b2b2b") #sets notification lable

    createFileButton = tk.Button(root, text="New File", command=lambda: newFilePopUp()) #sets new file button
    createFileButton.place(x=20, y=445) #places button

    deleteFileButton = tk.Button(root, text="Delete", command=lambda: deletePopUp(), state="disabled") #sets delete file button
    deleteFileButton.place(x=106, y=445) #places button

    renameFileButton = tk.Button(root, text="Rename", command=lambda: renamePopUp(), state="disabled") #sets rename file button
    renameFileButton.place(x=180, y=445) #places button

    undoLable = tk.Label(root, text="↩", fg="grey") #sets undo lable
    undoLable.place(x=280, y=449) #places lable
    undoLable.bind("<Button-1>", lambda e, lbl=undoLable, name="undo": safeUndo()) #binds undo function to when clicked

    redoLable = tk.Label(root, text="↪", fg="grey") #sets redo button
    redoLable.place(x=305, y=449) #places lable
    redoLable.bind("<Button-1>", lambda e, lbl=redoLable, name="undo": safeRedo()) #binds redo function to when clicked

    saveFileButton = tk.Button(root, text="Save", command=lambda: saveFile(), state="disabled") #sets ave file button
    saveFileButton.place(x=330, y=445) #places button

    binLable = tk.Label(root, text="🗑️") #sets bin label
    binLable.place(x=860, y=449) #places button

    logoutFileButton = tk.Button(root, text="Log Out", command=lambda: logout()) #sets log out button
    logoutFileButton.place(x=897, y=445) #places button

    filesLable = tk.Label(root, text="Files:", fg="grey") #sets files lable
    filesLable.place(x=20, y=0) #places lable

    fileTitle = tk.Label(root, text="", fg="grey") #sets opened file title
    fileTitle.place(x=280, y=0) #places lable

    unsavedMarker = tk.Label(root, text="", fg="grey") #sets unsaved marker lable
    unsavedMarker.place(x=915, y=0) #places lable

    notificationText = tk.Label(root, text="", fg="grey") #sets file editor notification text
    notificationText.place(x=400, y=449) #places lable

    fileFont = tkFont.Font(family="Helvetica", size=15, weight="bold") #file list font

    def updateUndoRedoState(): #function to check if undo/redo is available
        try:
            fileEditor.edit_undo() #attemps an undo
            fileEditor.edit_redo() #remove undo
            undoLable.config(fg="white") #changes lable to white (available)
        except:
            undoLable.config(fg="grey") #else changes it to grey (not available)

        try:
            fileEditor.edit_redo() #attemps an redo
            fileEditor.edit_undo() #removes redo
            redoLable.config(fg="white") #changes lable to white (available)
        except:
            redoLable.config(fg="grey") #else changes it to grey (not available)

    def safeUndo(): #undo function
        nonlocal unsaved
        try:
            fileEditor.edit_undo() #undo command
            unsaved = True #updates unsaved state
            markUnsaved() #marks a change has been made
        except:
            pass
        updateUndoRedoState() #updates undo/redo availability check

    def safeRedo(): #redo function
        nonlocal unsaved
        try:
            fileEditor.edit_redo() #redo command
            unsaved = True #updates unsaved state
            markUnsaved() #marks a change has been made
        except:
            pass
        updateUndoRedoState() #updates undo/redo availability check

    def markUnsaved(event=None): #display unsaved function
        nonlocal currentFileName,unsaved
        if currentFileName == None: #checks if a file is selected
            return #skips if not
        unsaved = True #updates unsaved state
        unsavedMarker.config(text=f"unsaved.") #displays unsaved state using lable

    def logout(): #logout function
        root.destroy() #closes menu window
        loginWindow(openMenuWin) #opens login window

    def loadFiles(): #function to loads user's files
        files = [f for f in Path(f"./users/{username}").glob("*.txt")] #loops though users directory looking for .txt files
        return files #returns file list

    def notification(message): #user notification function
        notificationText.config(text=message) #displays inputted text
        notificationText.after(2000, lambda: notificationText.config(text="")) #clears after 2000ms (2 seconds)

    def openFile(filename): #open file function
        nonlocal currentFileName, unsaved
        unsaved = False #resets unsaved variable
        notifyLable.config(text="") #clears center lable
        notifyLable.place_forget() #removes center lable
        currentFileName = filename #sets selected file as file currently open

        saveFileButton.config(state="normal") #enables save button
        deleteFileButton.config(state="normal") #enables delete button
        renameFileButton.config(state="normal") #enables rename button

        fileTitle.config(text=currentFileName) #sets filename title
        fileEditor.place(x=0, y=0) #places file editor

        try:
            data = file_utilities.loadFile(username, filename,key) #attempts to load data from file
        except (FileReadError, CryptoError) as e:
            notification(str(e)) #displays error if fail
            return #skips

        fileEditor.insert(tk.END, data) #places data

        if fileEditor.get("end-2c") == "\n": #checks for default new line being added
            fileEditor.delete("end-2c") #removes if found

        fileEditor.edit_reset() #resets undo/redo history
        updateUndoRedoState() #updates undo/redo availability

    def closeCurrentFile(): #close file function
        nonlocal currentFileName, unsaved
        saveFile() #saves file being closed
        fileEditor.edit_reset() #resets undo/redo history
        fileTitle.config(text="") #clears filename title

        undoLable.config(fg="grey") #greys undo button
        redoLable.config(fg="grey") #greys redo button
        saveFileButton.config(state="disabled") #disables save button
        deleteFileButton.config(state="disabled") #disables delete button
        renameFileButton.config(state="disabled") #disables rename button

        fileEditor.delete("0.0", "end") #clears editor
        fileEditor.place_forget() #closes editor
        unsaved = False #resets unsaved variable

    def fileClick(lable): #file click function
        nonlocal currentFileName
        notifyLable.config(text="") #clears center lable
        notifyLable.place_forget() #removes center lable
        filename = lable.cget("text")[2:]+".txt" #sets filename by removing lock symbol & adding file extension

        if currentFileName == filename: #checks if file open is the same as file being clicked
            return #skips if so
        else:
            closeCurrentFile() #otherwise, close current file
            openFile(filename) #open new file
            displayFiles() #refresh file display list
            return

    def displayFiles(): #display/update file list function
        nonlocal currentFileName
        files = loadFiles() #loads files

        for widget in fileList.winfo_children(): #loops though current file list
            widget.destroy() #clears each lable

        for f in files: #loop through each files
            filename = f.name #sets file name
            if currentFileName == filename: #checks which file is open
                icon = "🔓 " #sets lable to display file as open
                fg = "grey"
            else: #if file is not open
                icon = "🔒 " #sets lable to display file is closed
                fg = "white"

            fileLabel = tk.Label(fileList,text=icon+filename[:-4],font=fileFont,fg=fg,bg="#2b2b2b",pady=13,anchor="w",width=20,) #sets lable
            fileLabel.pack(fill="x", padx=10) #places lable

            border = tk.Frame(fileList, bg="#444444", height=1) #creates line divider
            border.pack(fill="x", padx=15) #places divider

            fileLabel.bind("<Button-1>", lambda e, lbl=fileLabel, name=filename: fileClick(lbl)) #sets file lable as clickable

        if len(files) == 0: #if no files are found
            notifyLable.place(relx=0.5, rely=0.5, anchor="center") #places center lable
            notifyLable.config(text="No Files! Select 'New File'.") #displays no files found
            return
        elif len(files) != 0 and currentFileName is None: #if files found but none selected
            notifyLable.place(relx=0.5, rely=0.5, anchor="center") #places center lable
            notifyLable.config(text="Select a File!") #displays no file selected

    def saveFile(): #save file function
        nonlocal unsaved
        if currentFileName is not None: #checks a file is currently open
            dataToSave = fileEditor.get("1.0", "end") #reads text editor
            unsaved = False #resets unsave variable
            unsavedMarker.config(text=f"") #clears marker

            try:
                file_utilities.writeFile(f"./users/{username}/{currentFileName}",dataToSave,key) #attempts to save to file
            except FileWriteError as e:
                notification(str(e)) #displays error if fails
                return #skips

            notification(f"{currentFileName} saved.") #shows saved notification

    def checkFileName(filename): #function to check if a file name exists
        files = [p.stem for p in loadFiles()] #loads user's files

        if filename == "": #if inputted file name is nothing
            error = "Enter File Name" #sets error
            return True, error #returns True and error
        elif filename in files: #if inputted file name is found in users existing files
            error = "File Already Exists" #sets error
            return True, error #returns True and error
        elif len(filename) > 20:  # if inputted file name is larger than 20 chars
            error = "File Name Too Large"  # sets error
            return True, error  # returns True and error
        else:
            return False #else returns false (no file name match is found and it is acceptable)

    def deletePopUp(): #delete file pop up window
        nonlocal currentFileName
        if currentFileName is None: #checks a file is currently open
            return #skips if not

        PopUp = tk.Toplevel(root) #creates window
        PopUp.title("File Delete") #window title
        PopUp.geometry("400x130") #window size
        center_window(PopUp) #centers pop up window
        PopUp.resizable(False, False) #disables ability to resize window
        PopUp.attributes("-fullscreen", False) #disables ability to full screen window

        PopUp.grab_set() #stops user from using menu window while open

        labelFont = tkFont.Font(family="Helvetica", size=14) #lable font
        titleFont = tkFont.Font(family="Helvetica", size=16, weight="bold") #title font

        popUpTitleLabel = tk.Label(PopUp, text=f"Confirm deleting {currentFileName}?", font=titleFont, fg="white") #delete message
        popUpTitleLabel.place(relx=0.5, rely=0.20, anchor="center") #places lable

        popUpLable = tk.Label(PopUp, text="Once a file is deleted, it is moved to the bin.", font=labelFont, fg="grey") #delete sub message
        popUpLable.place(relx=0.5, rely=0.50, anchor="center") #places lable

        cancelButton = tk.Button(PopUp, text="Cancel", command=lambda: PopUp.destroy()) #sets cancel button to close window
        cancelButton.place(relx=0.35, rely=0.80, anchor="center") #places button

        deleteButton = tk.Button(PopUp, text="Delete", command=lambda: deleteFile()) #sets delete button to delete function
        deleteButton.place(relx=0.65, rely=0.80, anchor="center") #places button

        PopUp.bind('<Return>', lambda e: deleteFile()) #binds enter/return to delete function

        def deleteFile(): #delete function (move to bin function)
            nonlocal currentFileName
            closeCurrentFile() #closes current file
            rename = f"{currentFileName}|  {datetime.datetime.now().strftime('%c')}.txt" #adds time stap to file name

            try:
                file_utilities.moveFile(f"./users/{username}/{currentFileName}",f"./users/{username}/bin/{rename}") #attemps to rename and move file to bin
            except FileWriteError as e:
                notification(str(e)) #displays error if fail
                return #skips

            notification(f"{currentFileName} deleted.") #displays file deleted
            currentFileName = None #resets current file variable

            PopUp.destroy() #closes delete popup
            displayFiles() #updates file list

        PopUp.wait_window() #stop menu window while file pop up open

    def renamePopUp(): #rename file pop up window
        nonlocal currentFileName
        if currentFileName is None: #if no file is selected
            return #skip

        PopUp = tk.Toplevel(root) #creates window
        PopUp.title("File Rename") #window title
        PopUp.geometry("400x130")  #window size
        center_window(PopUp) #centers pop up window
        PopUp.resizable(False, False) #disables ability to resize window
        PopUp.attributes("-fullscreen", False) #disables ability to full screen window

        PopUp.grab_set() #stops user from using menu window while open

        labelFont = tkFont.Font(family="Helvetica", size=14) #lable font

        popUpLabel = tk.Label(PopUp, text=f"Rename {currentFileName[:-4]}", font=labelFont, fg="white") #rename message
        popUpLabel.place(relx=0.5, rely=0.20, anchor="center") #place lable

        fileNameInput = tk.Entry(PopUp,width=25, bg="#2b2b2b", fg="white") #name input bpx
        fileNameInput.place(relx=0.5, rely=0.40, anchor="center") #place input box
        fileNameInput.insert(0,currentFileName[:-4]) #put current file name in input box (without extension)

        renameButton = tk.Button(PopUp, text="Rename", command=lambda: attemptFileRename()) #set rename button to rename function
        renameButton.place(relx=0.65, rely=0.80, anchor="center") #place rename button

        cancelButton = tk.Button(PopUp, text="Cancel", command=lambda: PopUp.destroy()) #set cancel button to close window
        cancelButton.place(relx=0.35, rely=0.80, anchor="center") #place cancel button

        errorLabel = tk.Label(PopUp, text="", font=labelFont, fg="red") #sets error lable
        errorLabel.place(relx=0.5, rely=0.60, anchor="center") #places lable

        def attemptFileRename(): #attemp rename function
            nonlocal currentFileName
            fileRename = f"{fileNameInput.get()}.txt" #fetches inputted filename (adds extension)
            check = checkFileName(fileRename[:-4]) #checks if filename is already taken

            if not check: #if filename is not taken
                saveFile() #save file
                closeCurrentFile() #close file

                currentFilePath = f"./users/{username}/{currentFileName}" #set old path
                newFilePath = f"./users/{username}/{fileRename}" #set new path

                try:
                    file_utilities.renameFile(currentFilePath, newFilePath) #attemp to rename file
                except FileWriteError as e:
                    notification(str(e)) #displays error if fail
                    return

                notification(f"{currentFileName} renamed to {fileRename}.") #notify user of successfully rename
                openFile(fileRename) #opens file (with new name)
                displayFiles() #updates file list
                PopUp.destroy() #closes pop up
            else: #if match is found
                fileNameInput.delete("0", "end") #clears inputted name
                errorLabel.config(text=check[1]) #displays check error

        PopUp.bind('<Return>', lambda event: attemptFileRename()) #binds enter/return to attempt rename

        PopUp.wait_window() #stop menu window while file pop up open

    def newFilePopUp(): #new file pop up window
        PopUp = tk.Toplevel(root) #creates window
        PopUp.title("New File") #window title
        PopUp.geometry("400x130") #window size
        center_window(PopUp) #centers pop up window
        PopUp.resizable(False, False) #disables ability to resize window
        PopUp.attributes("-fullscreen", False) #disables ability to full screen window
        PopUp.grab_set() #stops user from using menu window while open

        labelFont = tkFont.Font(family="Helvetica", size=14) #lable font

        popUpLabel = tk.Label(PopUp, text="New File Name", font=labelFont, fg="white") #sets new file message
        popUpLabel.place(relx=0.5, rely=0.20, anchor="center") #places label

        fileNameInput = tk.Entry(PopUp,width=25, bg="#2b2b2b", fg="white") #sets filename input box
        fileNameInput.place(relx=0.5, rely=0.40, anchor="center") #places input box

        createButton = tk.Button(PopUp, text="Create", command=lambda: attemptNewFile()) #sets create button to new file function
        createButton.place(relx=0.65, rely=0.80, anchor="center") #places button

        cancelButton = tk.Button(PopUp, text="Cancel", command=lambda: PopUp.destroy()) #sets cancel button to close window
        cancelButton.place(relx=0.35, rely=0.80, anchor="center") #places button

        errorLabel = tk.Label(PopUp, text="", font=labelFont, fg="red") #sets error lable
        errorLabel.place(relx=0.5, rely=0.60, anchor="center") #places error lable

        def attemptNewFile(): #create new file function
            nonlocal currentFileName

            inputName = fileNameInput.get() #fetch inputted file name
            check = checkFileName(inputName) #checks inputted file name

            if not check: #if no match found
                try:
                    saveFile() #save current file

                    try:
                        file_utilities.createFile(username,inputName,key) #attempt to create file
                    except FileWriteError as e:
                        notification(str(e)) #displays error if fail
                        return #skip

                    currentFileName = None #reset current file

                    fileTitle.config(text="") #clear file title
                    fileEditor.delete("1.0", "end") #clear text editor
                    fileEditor.place_forget() #remove text editor

                    openFile(f"{inputName}.txt") #open new file
                    notification(f"{inputName+".txt"} successfully created.") #notify user new file has been created

                    displayFiles() #update file list
                    PopUp.destroy() #close pop up
                except FileWriteError: #if creation fail
                    fileNameInput.delete("0", "end") #clear input box
                    errorLabel.config(text="Creation Failed, Try Again") #display error
            else: #if file name already taken
                fileNameInput.delete("0", "end") #clear input box
                errorLabel.config(text=check[1]) #displays check error

        PopUp.bind('<Return>', lambda e: attemptNewFile()) #bin enter/return to new file function
        PopUp.wait_window() #stop menu window while file pop up open

    displayFiles() #load file list

    root.bind('<Command-s>', lambda e: saveFile()) #bind command s to save file function
    root.bind('<Command-n>', lambda e: newFilePopUp()) #bind command n to new file function
    root.bind('<Command-r>', lambda e: renamePopUp()) #bind command r to rename file function

    fileEditor.bind("<Key>", markUnsaved) #update unsaved when a key is pressed in file editor
    fileEditor.bind("<KeyRelease>", lambda e: updateUndoRedoState()) #update undo/redo availability when a key is released in file editor
    fileEditor.bind('<Command-z>', lambda e: safeUndo()) #bind command z to undo function in file editor
    fileEditor.bind('<Command-y>', lambda e: safeRedo()) #bind command y to redo function in file editor

    root.mainloop() #set main menu (root) as main loop

loginWindow(openMenuWin) #calls login function to start the program