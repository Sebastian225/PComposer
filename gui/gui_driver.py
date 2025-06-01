import customtkinter
from tkinter import filedialog as fd

from gui.structure_editor_window import StructureEditorWindow


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("PComposer")
        self.structure_editor = None

        # add widgets to app
        self.button = customtkinter.CTkButton(self, command=self.button_click, text="Open a file")
        self.button.grid(row=0, column=0, padx=20, pady=10)

        self.button2 = customtkinter.CTkButton(self, command=self.open_structure_editor, text="Open structure editor")
        self.button2.grid(row=0, column=1, padx=20, pady=10)

    # add methods to app
    def button_click(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )
        # show the open file dialog
        f = fd.askopenfile(filetypes=filetypes)
        # read the text file and show its content on the Text
        print(f.readlines())

    def open_structure_editor(self):
        if self.structure_editor is None or not self.structure_editor.winfo_exists():
            self.structure_editor = StructureEditorWindow(self)  # create window if its None or destroyed
            self.structure_editor.after(10, self.structure_editor.focus)
        else:
            self.structure_editor.focus()  # if window exists focus it



