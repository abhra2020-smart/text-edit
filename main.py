from tkinter import *
from tkinter import filedialog
from tkinter import font

# Create Window
root = Tk()
root.title("TextEdit")
root.iconbitmap("C:\\Users\\abhra\\PycharmProjects\\CodeLegend\\TextEdit\\logo.png")
root.geometry("900x615")
global open_status_name
open_status_name = False

global selected
selected = False

validfiletypes = (
    ("Windows Text Document (*.txt)", "*.txt"),
    ("HTML Webpage (*.html)", "*.html"),
    ("Python Files (*.py)", "*.py"),
    ("Java Files (*.java)", "*.java"),
    ("C Files (*.c)", "*.c"),
    ("Executable File (*.exe)", "*.exe"),
    ("Windows Batch File (*.bat)", "*.bat"),
    ("ActionScript File (*.as)", "*.as"),
    ("Visual Basic File (*.vb)", "*.vb"),
    ("Visual Basic Script File (*.vbs)", "*.vbs")
)


# Create New File Function
def new_file():
    # Delete previous text
    text.delete(1.0, END)
    # Change Title
    root.title("TextEdit - New File")
    # Update Status Bar
    status_bar.config(text="New File        ")

    global open_status_name
    open_status_name = False


# Create Open File Function
def open_file():
    # Delete previous text
    text.delete("1.0", END)
    # Grab Filename
    text_file = filedialog.askopenfilename(
        initialdir="C:\\Users\\abhra\\PycharmProjects\\CodeLegend",
        title="Open File",
        filetypes=validfiletypes
    )
    if text_file:
        global open_status_name
        open_status_name = text_file
    name = text_file
    # Update Status bars
    status_bar.config(text=f"{name}        ")
    name = name.replace("C:\\Users\\abhra\\PycharmProjects\\CodeLegend", "")
    root.title(f"TextEdit - {name}")
    # Open File
    text_file = open(text_file, 'r')
    code = text_file.read()
    # Insert file content to textbox
    text.insert(END, code)
    # Close the opened file
    text_file.close()


# Create Save As Function
def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*",
                                             initialdir="C:\\Users\\abhra\\PycharmProjects\\CodeLegend",
                                             title="Save File As",
                                             filetypes=validfiletypes
                                             )
    if text_file:
        # Update Status bars
        name = text_file
        status_bar.config(text=f"Saved: {name}        ")
        name = name.replace("C:\\Users\\abhra\\PycharmProjects\\CodeLegend", "")
        root.title(f"TextEdit - {name}")

        # Save the file
        text_file = open(text_file, "w")
        text_file.write(text.get(1.0, END))
        # Close the file
        text_file.close()


# Create Save Function
def save_file():
    global open_status_name
    if open_status_name:
        # Save the file
        text_file = open(open_status_name, "w")
        text_file.write(text.get(1.0, END))
        # Close the file
        text_file.close()
        # Update status bar and popup
        newroot = Tk()
        newroot.title("Saved Successfully")
        newroot.geometry("400x400")
        success = Label(newroot, text="Saved")
        success.pack(newroot)
        status_bar.config(text=f"Saved: {open_status_name}        ")
    else:
        error = Tk()
        error.geometry("400x400")
        error.title("Unsuccessful save, try the save as option")


# Create Cut Function
def cut_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if text.selection_get():
            selected = text.selection_get()
            text.delete(SEL_FIRST, SEL_LAST)
            root.clipboard_clear()
            root.clipboard_append(selected)


# Create Copy Function
def copy_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    if text.selection_get():
        selected = text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected)


# Create Paste Function
def paste_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = text.index(INSERT)
            text.insert(position, selected)


# Create Main Frame
main_frame = Frame(root)
main_frame.pack(pady=5)

# Create Scrollbar For The Text Box
text_scroll = Scrollbar(main_frame)
text_scroll.pack(side=RIGHT, fill=Y)

# Create Text Box
text = Text(main_frame, width=100, height=25, font=("Consolas", 16),
            selectbackground="lightblue", selectforeground="black", undo=True,
            yscrollcommand=text_scroll.set)
text.pack()

# Configure Scrollbars
text_scroll.config(command=text.yview)

# Create Menu
menu = Menu(root)
root.config(menu=menu)

# Add File Menu
file_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Add Edit Menu
edit_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut                                           ", command=lambda: cut_text(False),
                      accelerator="Ctrl+X")
edit_menu.add_command(label="Copy                                          ", command=lambda: copy_text(False),
                      accelerator="Ctrl+C")
edit_menu.add_command(label="Paste                                         ", command=lambda: paste_text(False),
                      accelerator="Ctrl+V")
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=text.edit_undo, accelerator="Ctrl+Z")
edit_menu.add_command(label="Redo", command=text.edit_redo, accelerator="Ctrl+Y")

# Add Status Bar
status_bar = Label(root, text="Ready        ", anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)

# Edit bindings
root.bind("<Control-x>", cut_text)
root.bind("<Control-c>", copy_text)
root.bind("<Control-v>", paste_text)

root.mainloop()
