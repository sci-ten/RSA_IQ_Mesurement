'''
Created on 2020/06/05

@author: HIROTO
'''

import tkinter as tk

from GUI import gui_app

def main():
    root = tk.Tk()
    app = gui_app.Application(root)
    app.mainloop()


if __name__ == '__main__':
    main()



