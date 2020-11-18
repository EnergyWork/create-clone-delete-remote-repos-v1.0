import tkinter as tk
from tkinter.ttk import *

class About(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('350x100')
        self.title('About')
        self.iconbitmap(parent.path_to_label_image)
        self.resizable(0, 0)
        about_text = 'Program for craete, clone and delete remote repository\nCreated by EnergyWork\nGitHub: github.com/EnergyWork'
        lbl_about_text = Label(master=self, text=about_text)
        lbl_about_text.grid(column=0, row=0, padx=15, pady=15)
        parent.center_window(self)