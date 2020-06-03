'''
Created on 2020/06/02

@author: HIROTO
'''
import tkinter as tk
from tkinter import filedialog


class FrameScheduleExecutionMode(tk.Frame):
    def __init__(self,master=None):
        """
        master : object <class 'tkinter.Tk'>

        nextpage: object <class 'tkinter.Tk'>
            Transition destination page

        """
        super().__init__(master)

        self.create_widget()
        self.pack()


    def create_widget(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        #print out now Mode
        self.mode_var=tk.StringVar()
        self.mode_var.set("Schedule Execution Mode")
        self.label1=tk.Label(self.frame,textvariable=self.mode_var,font=("",20))
        self.label1.pack()

class FrameScheduleInputForm(tk.Frame):
    def __init__(self,master=None):
        """
        master : object <class 'tkinter.Tk'>

        nextpage: object <class 'tkinter.Tk'>
            Transition destination page

        """
        super().__init__(master)
        self.pack()
        self.create_widget()


    def create_widget(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.sche_input_form = tk.Frame(self.frame, relief=tk.RIDGE, bd=2)

        l1 = tk.Label(self.sche_input_form, text='Schedule Input Form',  bd=2)
        l1.grid(row=0, column=0, columnspan=1, padx=5, pady=5)
        self.schepath_entry=tk.Entry(self.sche_input_form)
        self.schepath_entry.insert(tk.END,"\C:")
        self.schepath_entry.grid(row=1, column=0, columnspan=1, padx=5, pady=5)
        #Open file explore
        sbutton=tk.Button(self.sche_input_form,text='...', command=self.sbutton_clicked)
        sbutton.grid(row=1, column=1, columnspan=1, padx=5, pady=5)
        self.sche_input_form.grid(row=0, column=0)

    def sbutton_clicked(self):
        sp = tk.Tk()
        sp.withdraw()
        sp.filename =  filedialog.askdirectory(initialdir = "/",title = "Select Directory")
        print (sp.filename)
        #self.savepath=sp.filename
        self.schepath_entry.delete(0, tk.END)
        self.schepath_entry.insert(tk.END,sp.filename)

class FrameScheduleSavePathForm(tk.Frame):
    def __init__(self,master=None):
        """
        master : object <class 'tkinter.Tk'>

        nextpage: object <class 'tkinter.Tk'>
            Transition destination page

        """
        super().__init__(master)
        self.pack()
        self.create_widget()
        self.pack()


    def create_widget(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.save_path_frame = tk.Frame(self.frame, relief=tk.RIDGE, bd=2)
        l1 = tk.Label(self.save_path_frame, text='TIQ save Directory',  bd=2)
        l1.grid(row=0, column=0, columnspan=1, padx=5, pady=5)
        self.savedir_entry=tk.Entry(self.save_path_frame)
        self.savedir_entry.insert(tk.END,"\C:")
        self.savedir_entry.grid(row=1, column=0, columnspan=1, padx=5, pady=5)
        #Open file explore
        sbutton=tk.Button(self.save_path_frame,text='...', command=self.sbutton_clicked)
        sbutton.grid(row=1, column=1, columnspan=1, padx=5, pady=5)
        self.save_path_frame.pack(padx=5, pady=5)

    def sbutton_clicked(self):
        sp = tk.Tk()
        sp.withdraw()
        sp.filename =  filedialog.askdirectory(initialdir = "/",title = "Select Directory")
        print (sp.filename)
        self.savepath=sp.filename
        self.savedir_entry.delete(0, tk.END)
        self.savedir_entry.insert(tk.END,sp.filename)




#Mesurement execution button
class RunBotton(tk.Frame):
    def __init__(self,master=None,schepath_entry=None,savedir_entry=None,mang_rsa=None,App=None):
        """
        master : object <class 'tkinter.Tk'>

        nextpage: object <class 'tkinter.Tk'>
            Transition destination page

        inputframe: object <class 'FrameParameterInput'>
            tkinter frame corresponds to the input form

        mange_rsa: object <class 'Control_RSA'>
            object to controll RSA
        """
        super().__init__(master)
        self.create_widget()
        self.schepath_entry=schepath_entry
        self.savedir_entry=savedir_entry

        self.mang_rsa=mang_rsa
        self.conf=mang_rsa.par
        self.App=App

        self.pack()

    def create_widget(self):
        rbutton=tk.Button(self,text='Run', command=self.run_button_clicked)
        rbutton.pack(padx=5, pady=5)

    def run_button_clicked(self):
        print("Run Sche")
        print(self.schepath_entry.get())
        print(self.savedir_entry.get())
