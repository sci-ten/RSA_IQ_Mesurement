'''
Created on 2020/06/02

@author: HIROTO
'''
import tkinter as tk
import sys

from GUI import menubar
from GUI import frame_simple_setting_mode
from GUI import frame_schedule_execution_mode

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.geometry("500x420")
        self.master.title("Mesurement Setting")
        self.master.app=self
        self.create_widget()

    def create_widget(self):

        #description this title one word
        self.frame = tk.Frame(self.master)
        self.title_var=tk.StringVar()
        self.title_var.set("IQ Streaming")
        self.title_label=tk.Label(self.frame, textvariable=self.title_var,font=("",25))
        self.title_label.pack()
        #self.frame.grid(row=0, column=0,sticky='NESW')
        self.frame.pack()

        self.page_pearent = tk.Frame(self.master)
        #self.frame2.grid(row=1, column=0)
        self.page_pearent.pack()



        #-------------------------------------
        # frame page.1
        #-------------------------------------
        self.page1= tk.Frame(self.page_pearent)
        self.simphead=frame_simple_setting_mode.FrameSimpleSettingMode(self.page1)
        self.simpform=frame_simple_setting_mode.FrameParameterInput(self.page1)
        self.simprunbotton=frame_simple_setting_mode.RunBotton(self.page1,self.simpform,self.master)
        self.page1.grid(row=0, column=0,sticky='NESW')
        #-------------------------------------
        # frame page.2
        #-------------------------------------
        self.page2= tk.Frame(self.page_pearent)
        self.Schephead=frame_schedule_execution_mode.FrameScheduleExecutionMode(self.page2)
        self.ScheState=frame_schedule_execution_mode.FrameNowState(self.page2)
        self.Scheform=frame_schedule_execution_mode.FrameScheduleInputForm(self.page2)
        self.Schesaveform=frame_schedule_execution_mode.FrameScheduleSaveForm(self.page2)
        self.Scherunbotton=frame_schedule_execution_mode.RunBotton(self.page2,self.Scheform.schepath_entry,self.Schesaveform.savedir_entry,self.Schesaveform.progdir_entry,self.master,self.ScheState)
        self.page2.grid(row=0, column=0,sticky='NESW')
        #-------------------------------------
        # Set Top Layer page
        #-------------------------------------
        self.page1.tkraise()

        page_list=[self.page1,self.page2]

        #add menu bar
        self.menubar_obj=menubar.Menubar(pagelist=page_list)
        self.master['menu']=self.menubar_obj

