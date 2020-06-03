'''
Created on 2020/06/02

@author: HIROTO
'''
import tkinter as tk


class Menubar(tk.Menu):
    def __init__(self,master=None,pagelist=None):
        super().__init__(master)
        self.create_menu_bar()
        self.pagelist=pagelist

    def create_menu_bar(self):
        menubar=tk.Menu(self)

        self.check_simple_mode = tk.BooleanVar()
        self.check_simple_mode.set(True)
        self.check_schedule_mode  = tk.BooleanVar()

        menubar.add_checkbutton(label="Simple Setting Mode", onvalue=1, offvalue=1, variable=self.check_simple_mode,command=self.onSimp)
        menubar.add_checkbutton(label="Schedule Execution Mode", onvalue=1, offvalue=1, variable=self.check_schedule_mode,command=self.onSche)
        self.add_cascade(label="Run Mode", menu=menubar)

    def onSimp(self):
        print("onSimp")
        self.check_schedule_mode.set(False)
        self.changePage(self.pagelist[0])



    def onSche(self):
        print("onShce")
        self.check_simple_mode.set(False)
        self.changePage(self.pagelist[1])

    def changePage(self, page):
        page.tkraise()


def main():
    root = tk.Tk()
    root['menu'] = Menubar()
    root.mainloop()

if __name__ == "__main__":
    main()

