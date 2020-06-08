'''
Created on 2020/06/04

@author: HIROTO
'''

import pandas as pd
import datetime
import re
import sched
import time
import os
from ctypes import *

from RSA_Controll import StreamIQ_ScheduleMesurement
from RSA_Controll import RSA_API
from RSA_Controll import time_adjust
from DB_ULDL import db_RsaMesurementParameter
from DB_ULDL import experiment_id
from DB_ULDL import LocalSave
from File_Checker import read_parameter_file
from DB_ULDL.LocalSave import LocalBackUp

class SchedulemManager():
    """
    Control Mesurement when run botton is clicked in schedule mode
    is pressed in GUI

    Attributes
    ---------------
    schepath: string
        csv which describes the mesurement schedule
    savedir: string
        directory to save TIQ file
    App: object <class'tkinter.Tk>
        top level gui object
    """
    def __init__(self,parameter,App,DB_uploader):
        self.schepath=parameter["schepath"]
        self.savedir=parameter["savedir"]
        self.App=App
        self.DB_uploader=DB_uploader

        #parse and sort
        self.schedule=ScheduleParser(self.schepath)
        self.schedule.parser_schedule()
        self.schedule.sort_schedule_timeline()

        #create TimeAdjust object
        self.timer=time_adjust.TimeAdjust()

        #Time Adjust
        if self.timer.standerd_time is None:
            self.timer=time_adjust.TimeAdjustOffline()
        self.timer.set_standerd_time()


        #Create table object
        self.rsa_prams_table=db_RsaMesurementParameter.MesurementParmsTable()

        #Create local back up object
        self.loc_bk=LocalSave.LocalBackUp(self.savedir)

        #set the RSA API path
        #os.chdir("C:\\Tektronix\\RSA_API\\lib\\x64")

        #Load RSA API
        #self.rsa=cdll.LoadLibrary("RSA_API.dll")

        #Create Controll RSA object
        #self.mang_rsa=StreamIQ_ScheduleMesurement.Control_RSA_ScheduleMesurement(self.rsa,self.timer,self.condb)

        self.mang_rsa=StreamIQ_ScheduleMesurement.Control_RSA_ScheduleMesurement(None,self.timer)


    def controll_mesurement(self):

        #Create Schedule Exsecution object
        s = sched.scheduler(self.timer.get_now_time_stamp, time.sleep)

        #Run schedule one by one
        for index, row in self.schedule.Schedule_df.iterrows():

            #get mesurement parameter
            df_para=read_parameter_file.read_parameter_csv(row['ParameterPath'])

            #set mesurement parameter parameter
            self.mag_rsa.par.set_parameter(self,cf=df_para['Center Freqency[Hz]'],refLevel=df_para['Reference Level[dBm]'],bw=df_para['Band Width[Hz]'],durationMsec=df_para['Sampling Rate[Hz]'],fileInterval=df_para['Make File Interval [sec]'],savedir=self.savedir)

            #make origunal experiment ID
            id=experiment_id.ExperimentID()

            if row['StartUnixTime']<=self.timer.get_now_time_stamp():

                #Wait for scheduled time and run
                s.enterabs(row['StartUnixTime'],1, self.mang_rsa.iq_stream, argument=(self,id,row))
                s.run()

                #Marge various mesurement information for pandas Series
                Series=self.rsa_prams_table.marge_ex_data_as_dfSeries(id,self.mang_rsa.timedic,self.savedir,self.mang_rsa.num,self.mang_rsa.par,'A')

                try:
                    self.DB_uploader.update_for_db(self,Series)
                except:
                    pass

                #Add
                self.rsa_prams_table.append_dfSeries(Series)

        self.loc_bk.save(self.rsa_prams_table.ms_parms_df)



class ScheduleParser():
    def __init__(self,path):
        self.date_format=DateFormat()
        self.time_format=TimeFormat()
        self.load_data_df=self.laod_schedule(path)
        self.Schedule_df=pd.DataFrame(columns=['StartTimeStamp','StartUnixTime','EndTimeStamp','ENDUnixTime','ParameterPath'])
        self.complite=True

    @staticmethod
    def laod_schedule(path):
        sche_df=pd.read_csv(path)
        return sche_df

    def parser_schedule(self):
        #Convert to specified format
        for index, row in self.load_data_df.iterrows():
            if row.isnull().any() ==False:

                startDate=self.format_timestamp(row['Start_Date'],self.date_format)
                startTime=self.format_timestamp(row['Start_Time'],self.time_format)
                endDate=self.format_timestamp(row['End_Date'],self.date_format)
                endTime=self.format_timestamp(row['End_Time'],self.time_format)
                #Check if date and time exists
                check_start=self.detect_invalid_timestamp(startDate,startTime)
                check_end=self.detect_invalid_timestamp(endDate,endTime)
                #Check if parameter path exists
                check_para=os.path.exists(row['ParameterPath'])

                if check_start and check_end and check_para==True:
                    #Combine Date and Time as Tiemstamp
                    startTimeStamp=startDate+startTime
                    endTimeStamp=endDate+endTime
                    #Convert datatime object
                    startTimeStampObj=datetime.datetime.strptime(startTimeStamp,"%Y/%m/%d %H:%M:%S")
                    endTimeStampObj=datetime.datetime.strptime(endTimeStamp,"%Y/%m/%d %H:%M:%S")

                    #add schedule to date frame
                    add=pd.Series([startTimeStamp,startTimeStampObj.timestamp(),endTimeStamp,endTimeStampObj.timestamp(),row['ParameterPath']],index=self.Schedule_df.columns)

                    self.Schedule_df=self.Schedule_df.append(add, ignore_index=True)
                else:
                    self.complite=False


    #Format date and time data
    def format_timestamp(self,data,format):
        #Check whether to accept data And convert to the desired number of digits
        if format.compiled_default_format.search(data) is not None:
            ex_part=format.compiled_default_format.search(data).group()
            value_list=re.split('\D',ex_part)
            str_timestamp=format.partition[0]
            #0 padding
            for idx,value in enumerate(value_list):
                str_timestamp+=value.zfill(format.digit_num_list[idx])
                if idx!=2:
                    str_timestamp+=format.partition[idx+1]
            return str_timestamp
        else:
            print(data,'cannot be accepted!')
        return None

    def detect_invalid_timestamp(self,date,time):
        if (date is not None) and (time is not None):
            datetime_str=date+time
        else:
            return False
        try:
            datetime.datetime.strptime(datetime_str,"%Y/%m/%d %H:%M:%S")
            return True
        except ValueError:
            return False

    def sort_schedule_timeline(self):
        self.Schedule_df=self.Schedule_df.sort_values(by='StartUnixTime')

class DateFormat():
    def __init__(self):
        self.default_format=r'\d{4}\D\d{1,2}\D\d{1,2}'
        self.compiled_default_format=re.compile(self.default_format)
        #eg. 2020/01/01
        self.digit_num_list=[4,2,2]
        self.partition=['','/','/','']


class TimeFormat():
    def __init__(self):
        self.default_format=r'\d{1,2}\D\d{1,2}\D\d{1,2}'
        self.compiled_default_format=re.compile(self.default_format)
        #eg. 12:05:10
        self.digit_num_list=[2,2,2]
        self.partition=[' ',':',':','']




