import tkinter as tk
import tkinter.filedialog as fd
from tkinter import messagebox
from tkinter.ttk import *
import github
from github import Github

class Auth(tk.Toplevel):
    parent = None
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.iconbitmap(parent.path_to_label_image)
        self.resizable(0, 0)
        lbl_auth_token = Label(master=self, text='Authentication token')
        lbl_auth_token.grid(column=0, row=0, sticky='w', padx=15, pady=5)
        token = tk.StringVar()
        ent_auth_token = Entry(master=self, textvariable=token, show='*', width=50)
        ent_auth_token.grid(column=0, row=1, sticky='w', padx=15, pady=5)
        btn_done = Button(master=self, text='Auth', command=lambda:self.auth(token.get()))
        btn_done.grid(column=0, row=2, padx=5, pady=5)
        self.parent.center_window(self)

    def auth(self, userlogin):
        try:
            self.parent.github_account = Github(login_or_token=userlogin)
            u = self.parent.github_account.get_user().login
            messagebox.showinfo('Authenticated', f'Hi {u}')
            self.parent.main_window.lbl_who['text'] = u
            self.parent.main_window.get_reposities()
            self.destroy()
        except github.BadCredentialsException:
            messagebox.showerror("ERROR", "Authentication error")
