'''
Created on 2020/06/02

@author: HIROTO
'''
import tkinter as tk
from tkinter import filedialog
import time
from GUI import initial_parameter
from Scheduller.Simple_Setting_Mode_Controll import *


#Header message
class FrameSimpleSettingMode(tk.Frame):
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
        self.mode_var.set("Simple Setting Mode")
        self.label1=tk.Label(self.frame,textvariable=self.mode_var,width=20,font=("",20))
        self.label1.pack(padx=5, pady=5)
        self.label2=tk.Label(self.frame, text='Measurement Config', bd=2)
        self.label2.pack()

#Measurement parameter form
class FrameParameterInput(tk.Frame):
    def __init__(self,master=None):
        """
        master : object <class 'tkinter.Tk'>

        nextpage: object <class 'tkinter.Tk'>
            Transition destination page

        """
        super().__init__(master)


        self.initpar=initial_parameter.Initial_Parameters()
        #Set Initial Parameter as last parameter
        self.dic_par=self.initpar.load_parameter()
        self.create_widget()
        self.pack()

    def create_widget(self):
        self.frame = tk.Frame(self.master)
        #Input form for Mesurement parameter
        self.input_form()
        #Inpur form for save TIQ path
        self.save_path_f()
        self.frame.pack()

    def input_form(self):
        self.input_frame = tk.Frame(self.frame, relief=tk.RIDGE, bd=2)
        #First Label
        self.input1=self.inputform_temp(text="Center Frequency[Hz]:",dicname="Center Freqency",row=0,initvalue='0.0')
        #Second Labe
        self.input2=self.inputform_temp(text='Reference Level[dBm]:',dicname='Reference Level',row=1,initvalue=0)
        # Third Label
        self.input3=self.inputform_temp(text='Band width[Hz]:',dicname='Band Width',row=2,initvalue=1.25e6)
        # Forth Label
        self.input4=self.inputform_temp(text='Duration [msec]:',dicname="Duration",row=3,initvalue=1000)
        # Fifth Label
        self.input5=self.inputform_temp(text='Wait time[sec]:',dicname="Wait Time",row=4,initvalue=0.0)
        # Sixth Label
        self.input6=self.inputform_temp(text='Make File Interval[sec]:',dicname="Make File Interval",row=4,initvalue=0.0)

        self.input_frame.pack()


    def inputform_temp(self,text,dicname,row,initvalue):
        l=tk.Label(self.input_frame, text=text, bd=2)
        l.grid(row=row, column=0, padx=5, pady=5)
        input=tk.Entry(self.input_frame)
        input.insert(tk.END,self.dic_par.get(dicname,initvalue))
        input.grid(row=row, column=1, columnspan=1, padx=5, pady=5)
        return input

    def save_path_f(self):
        self.save_path_frame = tk.Frame(self.frame, relief=tk.RIDGE, bd=2)
        l1 = tk.Label(self.save_path_frame, text='Save path',  bd=2)
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


    #get mesurement parameter from window
    def get_parameter_from_window(self):

        try:
            parameter={"cf":float(self.input1.get()),
                       "refLevel": float(self.input2.get()),
                       "bw": float(self.input3.get()),
                       "durationMsec": int(self.input4.get()),
                       "waitTime" : float(self.input5.get()),
                       "fileInterval" : float(self.input6.get()),
                       "savedir" : self.savedir_entry.get()
                       }
        except:
            print("cannottype change input data")
            parameter=None
        return parameter

#Mesurement execution button
class RunBotton(tk.Frame):
    def __init__(self,master=None,inputframe=None,App=None):
        """
        master : object <class 'tkinter.Tk'>

        nextpage: object <class 'tkinter.Tk'>
            Transition destination page

        inputframe: object <class 'FrameParameterInput'>
            tkinter frame corresponds to the input form
        """
        super().__init__(master)
        self.create_widget()
        self.inputframe=inputframe
        self.App=App

        self.pack()

    def create_widget(self):
        rbutton=tk.Button(self,text='Run', command=self.run_button_clicked)
        rbutton.pack(padx=5, pady=5)

    #Process when the execute button ON
    def run_button_clicked(self):
        #Get value from input form to set mesurement parameter
        parameter=self.inputframe.get_parameter_from_window()
        print("run",parameter)
        if parameter is None:
            self.failure_window()
            return

        self.runner=SimpleSettingMode(parameter)
        #Check parameter is not invalid
        self.app_state=self.runner.RunCheck()
        if not self.app_state:
            self.failure_window()
            return

        #Saved to use as initial parameter value at the next mesuremnt
        self.inputframe.dic_par=self.inputframe.initpar.make_dic(cf=parameter['cf'],refLevel=parameter['refLevel'],bw=parameter['bw'],durationMsec=parameter['durationMsec'],waitTime=parameter['waitTime'],fileInterval=parameter['fileInterval'])
        self.inputframe.initpar.save_parameter(self.inputframe.dic_par)

        print("観測開始")
        time.sleep(0.1)
        #Break GUI
        self.App.destroy()

        #Run IQ Streaming
        self.runner.Run()



    def failure_window(self):
        failwin=tk.Tk()
        failwin.geometry('150x100+100+300')
        label1 = tk.Label(
            failwin,
            text='Please try again setting',
            width=30,
            )

        label1.pack()


