import tkinter
import customtkinter

keys_list = ["Tonic", "Dominant", "Relative", "Dominant relative", "Subdominant"]
keys_notations = {
    "Tonic": "T",
    "Dominant": "D",
    "Relative": "R",
    "Dominant relative": "DR",
    "Subdominant": "SD"
}

parts_pieces_list = ["Subject", "Answer", "Countersubject 1", "Countersubject 2", "Free counterpoint", "Empty"]
parts_pieces_notation = {
    "Subject": "S",
    "Answer": "A",
    "Countersubject 1": "CS1",
    "Countersubject 2": "CS2",
    "Free counterpoint": "FC",
    "Empty": "E"
}


class GridFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, keys, parts, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

        self.keys = keys
        self.parts = parts
        self.number_of_pieces = 1

        self.combobox = customtkinter.CTkOptionMenu(self, values=keys_list)
        self.combobox.set("Tonic")
        self.combobox.grid(row=0, column=1, padx=10, pady=10)


class ControlFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.number_of_countersubjects = 2
        self.columnconfigure(5, weight=2)

        self.parts_number = tkinter.IntVar(value=3)
        self.radio1 = customtkinter.CTkRadioButton(self, text="3 parts",
                                                   command=self.radiobutton_event, variable=self.parts_number, value=3)
        self.radio1.grid(row=0, column=0, padx=10, pady=10)
        self.radio2 = customtkinter.CTkRadioButton(self, text="4 parts",
                                                   command=self.radiobutton_event, variable=self.parts_number, value=4)
        self.radio2.grid(row=0, column=1, padx=10, pady=10)

        self.label = customtkinter.CTkLabel(self, text=f"Number of counter subjects: {self.number_of_countersubjects}", fg_color="transparent")
        self.label.grid(row=0, column=2, padx=10, pady=10)

        self.slider = customtkinter.CTkSlider(self, from_=1, to=9, command=self.slider_event)
        self.slider.grid(row=0, column=3, padx=10, pady=10)
        self.slider.set(2)

        self.button = customtkinter.CTkButton(self, text="Import")
        self.button.grid(row=0, column=4, padx=10, pady=10)

        self.button2 = customtkinter.CTkButton(self, text="Generate")
        self.button2.grid(row=0, column=5, padx=10, pady=10, sticky="e")

    def radiobutton_event(self):
        print("radiobutton toggled, current value:", self.parts_number.get())

    def slider_event(self, value):
        self.number_of_countersubjects = int(value)
        self.label.configure(text=f"Number of counter subjects: {self.number_of_countersubjects}")


class StructureEditorWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.keys = []
        self.parts = [[], [], []]

        self.geometry("1200x900")
        self.title("Structure editor")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.grid_frame = GridFrame(self, keys=self.keys, parts=self.parts,
                                    orientation="horizontal")
        self.grid_frame.grid(row=0, column=0, sticky="nsew")

        self.control_frame = ControlFrame(self)
        self.control_frame.grid(row=1, column=0, sticky="ew")
