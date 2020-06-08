'''
Created on 2020/06/02

@author: HIROTO
'''
import tkinter as tk
from tkinter import filedialog

#Local Library
from File_Checker import format_check
from Scheduller import main_controll


class FrameScheduleExecutionMode(tk.Frame):
    def __init__(self,master=None):
        """
        master: object <class 'tkinter.Tk'>

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

        l1 = tk.Label(self.sche_input_form, text='Mesurement schedule file path',  bd=2)
        l1.grid(row=0, column=0, columnspan=1, padx=15, pady=8)
        self.schepath_entry=tk.Entry(self.sche_input_form)
        self.schepath_entry.insert(tk.END,"\C:")
        self.schepath_entry.grid(row=1, column=0, columnspan=1, padx=15, pady=8)
        #Open file explore
        sbutton=tk.Button(self.sche_input_form,text='...', command=self.sbutton_clicked)
        sbutton.grid(row=1, column=1, columnspan=1, padx=15, pady=8)
        self.sche_input_form.grid(row=0, column=0)

    def sbutton_clicked(self):
        sp = tk.Tk()
        sp.withdraw()
        sp.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select Directory")
        print (sp.filename)
        #self.savepath=sp.filename
        self.schepath_entry.delete(0, tk.END)
        self.schepath_entry.insert(tk.END,sp.filename)

class FrameScheduleSaveForm(tk.Frame):
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
        l1.grid(row=0, column=0, columnspan=1, padx=15, pady=8)
        self.savedir_entry=tk.Entry(self.save_path_frame)
        self.savedir_entry.insert(tk.END,"\C:")
        self.savedir_entry.grid(row=1, column=0, columnspan=1, padx=15, pady=8)

        self.prog_path_frame = tk.Frame(self.frame, relief=tk.RIDGE, bd=2)
        l2 = tk.Label(self.prog_path_frame, text='Mesurement Progress save Directory',bd=2)
        l2.grid(row=0, column=0, columnspan=1, padx=15, pady=8)
        self.progdir_entry=tk.Entry(self.prog_path_frame)
        self.progdir_entry.insert(tk.END,"\C:")
        self.progdir_entry.grid(row=1, column=0, columnspan=1, padx=15, pady=8)

        #Open file explore
        sbutton1=tk.Button(self.save_path_frame,text='...', command=self.sbutton_clicked1)
        sbutton1.grid(row=1, column=1, columnspan=1, padx=15, pady=8)
        self.save_path_frame.pack(padx=5, pady=5)
        sbutton2=tk.Button(self.prog_path_frame,text='...', command=self.sbutton_clicked2)
        sbutton2.grid(row=1, column=1, columnspan=1, padx=15, pady=8)
        self.prog_path_frame.pack(padx=5, pady=5)

    def sbutton_clicked1(self):
        sp = tk.Tk()
        sp.withdraw()
        sp.filename =  filedialog.askdirectory(initialdir = "/",title = "Select Directory")
        print (sp.filename)
        #self.savepath=sp.filename
        self.savedir_entry.delete(0, tk.END)
        self.savedir_entry.insert(tk.END,sp.filename)

    def sbutton_clicked2(self):
        sp = tk.Tk()
        sp.withdraw()
        sp.filename =  filedialog.askdirectory(initialdir = "/",title = "Select Directory")
        print (sp.filename)
        #self.savepath=sp.filename
        self.progdir_entry.delete(0, tk.END)
        self.progdir_entry.insert(tk.END,sp.filename)


class FrameNowState(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.pack()
        self.create_widget()
        self.pack()

    def create_widget(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.mode_var=tk.StringVar()
        self.mode_var.set("Now State: Waiting for Input")
        self.label1=tk.Label(self.frame,textvariable=self.mode_var,font=("",18))
        self.label1.pack(padx=5, pady=10)



#Mesurement execution button
class RunBotton(tk.Frame):
    def __init__(self,master=None,schepath_entry=None,savedir_entry=None,progdir_entry=None,App=None,frame_nowState=None):
        """
        master : object <class 'tkinter.Tk'>

        schepath : object <class 'tkinter.Tk'>
            tkinter entry to input directory of loding csv discribed mesurement schedule

        savedir: object <class 'tkinter.Tk'>
            tkinter entry to input directory of saving TIQ file

        progdir: object <class 'tkinter.Tk'>
            tkinter entry to input directory of saving mesurement progress

        App: object <class 'tkinter.Tk'>
            top level GUI application

        frame_nowState <class 'tkinter.Tk'>
            tkinter frame which has label to display the current app status
        """
        super().__init__(master)
        self.create_widget()
        self.schepath_entry=schepath_entry
        self.savedir_entry=savedir_entry
        self.progdir_entry=progdir_entry

        self.App=App
        self.frame_nowState=frame_nowState

        self.pack()

    def create_widget(self):
        rbutton=tk.Button(self,text='Run', command=self.run_button_clicked)
        rbutton.pack(padx=5, pady=5)

    def run_button_clicked(self):
        print("--Run Schedule Mode--")
        print(self.schepath_entry.get())
        print(self.savedir_entry.get())
        #Get value from input form to set mesurement parameter
        schepath=self.schepath_entry.get()
        savedir=self.savedir_entry.get()
        progdir=self.progdir_entry.get()
        #check file are exsist and file extension is correct
        file_check=format_check.check_paths_or_dirs_exsist([schepath,schepath,progdir])
        extension=format_check.check_file_extention(schepath,extention='csv')
        if file_check and  extension==False:
            self.failure_window()
            return 0

        #Change App status
        self.frame_nowState.mode_var.set("Now State: Waiting for Mesurement Start Time")

        parameter={"schepath":schepath,"savedir":savedir,"progdir":progdir}
        self.runner=main_controll.MesurementMainControll(mode='A',App=self.App,parameter=parameter)
        self.runner.run()

        #Finished
        self.App.destroy()

    def failure_window(self):
        failwin=tk.Tk()
        failwin.geometry('150x100+100+300')
        label1 = tk.Label(
            failwin,
            text='Please try again setting',
            width=30,
            )

        label1.pack()
