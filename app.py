import os, re
import tkinter as tk
from mainwindow import MainWindow
from auth import Auth
from about import About
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process


class App(tk.Tk):
    main_window = None
    github_account = None
    path_to_label_image = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'angleicon.ico')

    def __init__(self):
        super().__init__()
        self.title('Simple repository manipulation')
        self.iconbitmap(self.path_to_label_image)
        self.config(menu=self.craete_menu())
        self.resizable(0, 0)
        self.main_window = MainWindow(self)
        self.main_window.grid(column=0, row=0, padx=15, pady=15)
        self.center_window(self)
    
    def set_window_ccrr(self):
        self.main_window.set_window_ccrr()

    def set_window_drr(self):
        self.main_window.set_window_drr()

    def craete_menu(self):
        menu = tk.Menu(self, tearoff=0)
        sub_menu = tk.Menu(menu, tearoff=0)
        choose_program = tk.Menu(sub_menu, tearoff=0)
        choose_program.add_command(label='Create/Clone remote repos', command=self.set_window_ccrr)
        choose_program.add_command(label='Delete remote repos', command=self.set_window_drr)
        sub_menu.add_command(label='Auth', command=self.auth_window_via_token)
        sub_menu.add_cascade(label='Program', menu=choose_program)
        sub_menu.add_separator()
        sub_menu.add_command(label='Exit', command=self.destroy)
        menu.add_cascade(label='Menu', menu=sub_menu)
        menu.add_command(label='About', command=self.about_window)
        return menu
    
    def center_window(self, window):
        w, h, sx, sy = map(int, re.split(r'x|\+', window.winfo_geometry()))
        sw = (window.winfo_rootx() - sx) * 2 + w
        sh = (window.winfo_rooty() - sy) + (window.winfo_rootx() - sx) + h
        sx = (window.winfo_screenwidth() - sw) // 2
        sy = (window.winfo_screenheight() - sh) // 2
        window.wm_geometry('+%d+%d' % (sx, sy))

    def auth_window_via_token(self):
        auth_form = Auth(self)
        auth_form.grab_set()

    def about_window(self):
        about_form = About(self)
        about_form.grab_set()


if __name__ == "__main__":
    app = App()
    app.mainloop()
