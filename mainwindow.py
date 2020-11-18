import os

import tkinter as tk
import tkinter.filedialog as fd
from tkinter import messagebox
import tkinter.ttk as ttk

import pygit2
import github
from github import Github

class MainWindow(tk.Frame):
    choosed_program = 0
    parent = None

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.lbl_repos_name = ttk.Label(master=self, text='Repository name')
        self.lbl_repos_name.grid(column=0, row=0, sticky='w', padx=5, pady=5)

        self.cbox_repository = ttk.Combobox(master=self,width=47)
        self.cbox_repository.grid(column=0, row=1, sticky='w', padx=5, pady=5)

        self.layout_h = tk.Frame(master=self)
        
        self.bl_clone_it = tk.BooleanVar()
        self.chkbtn_clone_it = ttk.Checkbutton(master=self.layout_h, text='Clone it?', variable=self.bl_clone_it, onvalue=True, offvalue=False, command=self.clone_it)
        self.chkbtn_clone_it.grid(column=0, row=0)

        self.btn_choose_dir = ttk.Label(master=self.layout_h, text='choose a directory', font="Verdana 8 underline", foreground='blue', cursor='hand2')
        self.btn_choose_dir.bind('<Button-1>', self.choose_dir)
        self.btn_choose_dir.bind('<Enter>', self.on_enter)
        self.btn_choose_dir.bind('<Leave>', self.on_leave)

        self.layout_h.grid(column=0, row=2, sticky='w', padx=5, pady=5)

        self.ent_clone_to = ttk.Entry(master=self, width=50, state=tk.DISABLED)
        self.ent_clone_to.grid(column=0, row=3, sticky='w', padx=5, pady=5)

        self.btn_done = ttk.Button(master=self, text='Create repository', command=self.done)
        self.btn_done.grid(column=0, row=4, padx=5, pady=5)

        self.lbl_who = ttk.Label(master=self, text='Not authenticated', foreground='gray')
        self.lbl_who.grid(column=0, row=5, padx=0, pady=0)

    def clone_it(self):
        if self.bl_clone_it.get():
            self.chkbtn_clone_it['text'] = 'Clone to:'
            self.ent_clone_to['state'] = tk.NORMAL
            self.btn_done['text'] = 'Create and clone repository'
            self.btn_choose_dir.grid(column=1, row=0)
        else:
            self.chkbtn_clone_it['text'] = 'Clone it?'
            self.ent_clone_to['state'] = tk.DISABLED
            self.btn_done['text'] = 'Create repository'
            self.btn_choose_dir.grid_forget()

    def on_enter(self, e):
        self.btn_choose_dir['foreground'] = '#3a5ae8'

    def on_leave(self, e,):
        self.btn_choose_dir['foreground'] = '#122faa'

    def choose_dir(self, e):
        directory = fd.askdirectory(title='Выбирете директорию', initialdir='/')
        self.ent_clone_to.delete(0, last=tk.END)
        self.ent_clone_to.insert(0, directory)

    def set_window_ccrr(self):
        self.choosed_program = 0
        self.btn_done['text'] = 'Create repository'
        self.layout_h.grid(column=0, row=2, sticky='w', padx=5, pady=5)
        self.ent_clone_to.grid(column=0, row=3, sticky='w', padx=5, pady=5)

    def set_window_drr(self):
        self.choosed_program = 1
        self.btn_done['text'] = 'Delete'
        self.layout_h.grid_forget()
        self.ent_clone_to.grid_forget()

    def get_reposities(self):
        repos_list = []
        for repo in self.parent.github_account.get_user().get_repos():
            repos_list.append(repo.name)
        self.cbox_repository['values'] = repos_list

    def ccrr(self):
        repo_name = self.cbox_repository.get()
        if not (repo_name and not repo_name.isspace()):
            messagebox.showerror('ERROR', 'Repository name field is empty!')
            return
        clone = self.bl_clone_it.get()
        try:
            repo = self.parent.github_account.get_user().create_repo(name=repo_name, homepage='https://github.com')
            if clone:
                clone_path = self.ent_clone_to.get()
                clone_path = os.path.join(clone_path, repo_name)
                try:
                    _ = pygit2.clone_repository(repo.git_url, clone_path)
                except Exception as e:
                    messagebox.showerror('ERROR', f"{e.__class__}")
        except github.GithubException as e:
            if e.status == 422 and clone:
                ans = messagebox.askyesno('WARNING', f"Code: {e.status}, {e.data['message']}\n{e.data['errors'][0]['message']}\nClone?")
                if ans:
                    repo = self.parent.github_account.get_user().get_repo(name=repo_name)
                    clone_path = self.ent_clone_to.get()
                    clone_path = os.path.join(clone_path, repo_name)
                    try:
                        _ = pygit2.clone_repository(repo.git_url, clone_path)
                        messagebox.showinfo('Info', f'Cloned to {clone_path}')
                    except Exception as e:
                        messagebox.showerror('ERROR', f"{e.__class__}")
            else:
                messagebox.showerror('ERROR', f"Code: {e.status}, {e.data['message']}\n{e.data['errors'][0]['message']}")
        else:
            messagebox.showinfo('Success', 'success')

    def drr(self):
        repo_name = self.cbox_repository.get()
        try:
            repo = self.parent.github_account.get_user().get_repo(repo_name)
            repo.delete()
        except github.GithubException as e:
            messagebox.showerror('Deleting error', f"Code: {e.status}\n{e.data['message']}")
        else:
            messagebox.showinfo('Success', 'success')

    def done(self):
        if self.parent.github_account is None:
            messagebox.showerror('ERROR', "You're not authenticated!\nMenu > Auth > insert you auth token")
            return
        if self.bl_clone_it.get():
            if not (self.ent_clone_to.get() and not self.ent_clone_to.get().isspace()):
                messagebox.showerror('ERROR', "Choose a directory to clone")
                return
        if self.choosed_program == 0:
            self.ccrr()
        elif self.choosed_program == 1:
            self.drr()
        else:
            self.destroy()
