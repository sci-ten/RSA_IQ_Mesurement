'''
Created on 2020/06/07

@author: HIROTO
'''

import time
import tkinter as tk

from DB_ULDL import db_RsaMesurementParameter

class SingnInDatabaseForm(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master.title('Sign in form')
        self.dbinfo=db_RsaMesurementParameter.DBinfo()
        self.create_widget()
        self.pack()

    def create_widget(self):
        self.frame = tk.Frame(self, relief=tk.RIDGE)
        self.frame.pack()
        self.label1=self.inputform_temp(text="User Name",dicname="User Name",row=0,initvalue='0.0')
        self.label2=self.inputform_temp(text="Host Name or IP address",dicname="HostName",row=1,initvalue='0.0')
        self.label3=self.inputform_temp(text="Password",dicname="Password",row=2,initvalue='0.0',option='*')
        self.label4=self.inputform_temp(text="Database Name",dicname="DatabaseName",row=3,initvalue='0.0')
        self.button=SignInButton(self,self.master)

        self.button.pack()

    def inputform_temp(self,text,dicname,row,initvalue,option=None):
        l=tk.Label(self.frame, text=text, bd=2)
        l.grid(row=row, column=0, padx=5, pady=5)
        input=tk.Entry(self.frame,show=option)
        input.grid(row=row, column=1, columnspan=1, padx=5, pady=5)
        return input

    def set_to_dic(self):
        self.dbinfo.dic["UserName"]=self.label1.get()
        self.dbinfo.dic["HostName"]=self.label2.get()
        self.dbinfo.dic["Password"]=self.label3.get()
        self.dbinfo.dic["DatabaseName"]=self.label4.get()
        print(self.dbinfo.dic)
        #set dbinfo flag=True
        self.dbinfo.flag_on()


class SignInButton(tk.Frame):
    def __init__(self,master=None,App=None):
        super().__init__(master)
        self.App=App
        self.create_widget()
        self.pack()

    def create_widget(self):
        self.frame = tk.Frame(self,bd=2)
        cancel_button = tk.Button(self.frame,text='Cancel',command=self.Cancel_clicked)
        cancel_button.grid(row=0,column=0,columnspan=1,padx=25)
        sign_in_button = tk.Button(self.frame,text='Sign in',command=self.SighIn_clicked, bg='#F0F8FF')
        sign_in_button.grid(row=0,column=3,columnspan=1,padx=25)
        self.frame.pack()

    def SighIn_clicked(self):
        self.master.set_to_dic()
        time.sleep(0.1)
        self.App.destroy()

    def Cancel_clicked(self):
        print(self.master.dbinfo.dic)
        time.sleep(0.1)
        self.App.destroy()

