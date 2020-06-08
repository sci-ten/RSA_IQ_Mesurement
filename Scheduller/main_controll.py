'''
Created on 2020/06/08

@author: HIROTO
'''
import tkinter as tk
import time

from Scheduller import Simple_Setting_Mode_Controll
from Scheduller import mesurement_schedule
from DB_ULDL import db_RsaMesurementParameter
from GUI import DB_sign_in

class MesurementMainControll():
    def __init__(self,mode,App,parameter):
        self.mode=mode
        self.App=App
        self.mode=mode
        self.db_dic=None
        self.parameter=parameter

    def run(self):
        #Processing case of schedule execution mode
        if self.mode =='A':
            #get DataBase Sign in information form GUI
            self.get_db_info()
            #Create connect DataBase object
            self.condb=db_RsaMesurementParameter.ConnectDB(self.db_dic)
            #Create DataBase uploader object
            self.DB_uploader=db_RsaMesurementParameter.UpdateMesurementParms(self.condb.engine)
            #Create Mesurement Scheduller
            sche=mesurement_schedule.SchedulemManager(self.parameter,self.App,self.DB_uploader)
            #Exsecute Mesuement program according to schedule
            sche.controll_mesurement()


        #Processing case of Simple setting mode
        elif self.mode =='S':
            print("観測開始")
            time.sleep(0.1)
            self.runner=Simple_Setting_Mode_Controll.SimpleSettingMode(self.parameter)

            #Check parameter is not invalid
            self.app_state=self.runner.RunCheck()
            if self.app_state==False:
                return False

            #Break GUI
            self.App.destroy()
            #Run IQ Streaming
            self.runner.Run()


    def get_db_info(self):
        try:
            self.db_dic=self.App.menubar_obj.bar_DB.sign_in_frame.dbinfo
        except AttributeError:
            #Open DB Sign in form
            form=tk.Tk()
            db=DB_sign_in.SingnInDatabaseForm(form)
            db.mainloop()
            if db.dbinfo.flag==True:
                self.db_dic=db.dbinfo.dic
            else:
                return

def main():
    root = tk.Tk()
    app = MesurementMainControll('A',root)



if __name__ == '__main__':
    main()
