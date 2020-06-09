'''
Created on 2020/06/04

@author: HIROTO
'''
import csv
import os

#local library
from RSA_Controll import time_adjust

class MesurementProgress():
    def __init__(self,savedir,filename=r"mesurement_progress.csv"):
        self.savedir=savedir
        self.savepath=os.path.join(self.savedir,filename)



    def add_mesuremnt_log(self,nowUnixTime,tiqname):
        #convert now standard time stamp from unixtime
        nowTime=time_adjust.convert_datetime(nowUnixTime)
        time_str=time_adjust.convert_string_timestamp_to_milli(nowTime)

        Headers=["TimeStamp[sec]","UnixTime[sec]","TIQfilename"]
        contents={"TimeStamp[sec]":time_str,"UnixTime[sec]":nowUnixTime,"TIQfilename":tiqname}


        #If the file does not exist, make file and add a header
        if not os.path.exists(self.savepath):
            with open(self.savepath,'w', newline="") as f:
                writer = csv.DictWriter(f, fieldnames=Headers)
                writer.writeheader()
        #add contents to csv
        with open(self.savepath,'a', newline="") as f:
            writer = csv.DictWriter(f, fieldnames=Headers)
            writer.writerow(contents)


"""
savedir=r"D:\test"
m=MesurementProgress(savedir)
x=time_adjust.TimeAdjust()
nowUnixTime=x.get_now_time_stamp()
m.add_mesuremnt_log(nowUnixTime, "1")
"""