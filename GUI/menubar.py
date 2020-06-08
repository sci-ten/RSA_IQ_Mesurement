'''
Created on 2020/06/02

@author: HIROTO
'''
import tkinter as tk
from GUI import DB_sign_in


class Menubar(tk.Menu):
    def __init__(self,master=None,pagelist=None):
        super().__init__(master)
        self.pagelist=pagelist
        self.create_widget()

    def create_widget(self):
        menubar=tk.Menu(self)
        self.bar_RunMode=BarRunMode(menubar,self.pagelist)
        self.bar_DB=BarDB(menubar)

        self.add_cascade(label="Run Mode", menu=self.bar_RunMode.mode_bar)
        self.add_cascade(label="Database", menu=self.bar_DB.db_bar)

class BarRunMode(tk.Menu):
    def __init__(self,master=None,pagelist=None):
        super().__init__(master)
        self.pagelist=pagelist
        self.create_widget()

    def create_widget(self):
        self.mode_bar= tk.Menu(self)
        self.check_simple_mode = tk.BooleanVar()
        self.check_simple_mode.set(True)
        self.check_schedule_mode  = tk.BooleanVar()

        self.mode_bar.add_checkbutton(label="Simple Setting Mode", onvalue=1, offvalue=1, variable=self.check_simple_mode,command=self.onSimp)
        self.mode_bar.add_checkbutton(label="Schedule Execution Mode", onvalue=1, offvalue=1, variable=self.check_schedule_mode,command=self.onSche)

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

class BarDB(tk.Menu):
    def __init__(self,master=None):
        super().__init__(master)
        self.create_widget()
        self.sign_in_frame=None

    def create_widget(self):
        self.db_bar= tk.Menu(self)
        self.db_bar.add_command(label='Setting',command=self.db_setting)

    def db_setting(self):
        db_input_form=tk.Tk()
        self.sign_in_frame=DB_sign_in.SingnInDatabaseForm(db_input_form)



