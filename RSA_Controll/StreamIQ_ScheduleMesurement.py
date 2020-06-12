'''
Created on 2020/06/05

@author: HIROTO
'''
import time

from RSA_Controll.StreamIQ import *
from RSA_Controll.time_adjust import *
from RSA_Controll.Mesurement_log import *

from File_Checker.filename_check import *
# C:\Tektronix\RSA_API\lib\x64 needs to be added to the
# PATH system environment variable


class Control_RSA_ScheduleMesurement(Control_RSA):
    """
    Class related to RSA control (IQ streaming) which
    measure spectrum according to schedule

    Attributes
    ---------------
    par : object <class Config_parameter>
        Mesurement parameters
    rsa : object <class 'ctypes.CDLL'>
        RSA api object loaded with ctypes
    timer: object <class 'TimeAdjust'>
        Set the time correctly
    tsche: object <class 'ScheduleParser'>

    """
    def __init__(self,rsa,timer=None):
        """
        Parameters
        -------------------
        rsa: object <class 'ctypes.CDLL'>
            RSA api object loaded with ctypes
        timer: object <class 'TimeAdjust'>
            Set the time correctly
        """
        super().__init__(rsa,timer)
        self.timer=timer
        self.timedic={'StartTime':None,'StartUnixTime':None,'EndTime':None,'EndUnixTime':None}
        self.num=0

    def set_timer(self,timer):
        self.timer=timer

    def iq_stream(self,id,schdule,progdir,app):
        app.quit()
        self.progdir=progdir
        """
        Run IQ Streaming according to schedule
        """
        print("###### IQ Stream #####")
        #search device and connect
        Control_RSA.search_connect(self.rsa)
        #setting export type
        self.par.set_dest(IQSOUTDEST.IQSOD_FILE_TIQ)
        #setting measurement parameter to RSA
        self.config_iq_stream()

        #Mesurement Progress Report object
        self.prog=MesurementProgress(self.progdir)

        #save measuremant parameter
        #self.par.export_parameter_csv_with_time()

        self.id=id
        self.schdule=schdule

        ##Run RSA device
        self.rsa.DEVICE_Run()

        #get_now_time_stamp
        self.timedic['StartUnixTime']=self.timer.get_now_time_stamp()
        starttime=convert_datetime(self.timedic['StartUnixTime'])
        self.timedic['StartTime']=convert_string_timestamp(starttime)

        #IQ streaming Loop part
        self.Streaming_loop_processing()

        self.timedic['EndUnixTime']=self.timer.get_now_time_stamp()
        endtime=convert_datetime(self.timedic['EndUnixTime'])
        self.timedic['EndTime']=convert_string_timestamp(endtime)

    def Streaming_loop_processing(self):
        self.num=0
        while True:
            print(self.num)
            fileName = str(self.num+1)
            filenameBase = os.path.join(self.par.savedir,fileName)
            self.rsa.IQSTREAM_SetDiskFilenameBase(c_char_p(filenameBase.encode()))
            complete = c_bool(False)
            writing = c_bool(False)
            #Start IQstreaming
            self.rsa.IQSTREAM_Start()

            tiqname=get_latest_file(self.par.savedir,extension='tiq')
            nowUnixTime=self.timer.get_now_time_stamp()
            self.prog.add_mesuremnt_log(nowUnixTime,tiqname,self.id)

            flag=True
            #Case of complete.value==False,->continuous mesurement.
            while not complete.value:
                #Monitor streaming progress.If time passes more than durationMsec,then complete=True.
                self.rsa.IQSTREAM_GetDiskFileWriteStatus(byref(complete), byref(writing))
                """
                if flag==True:
                    #add mesuremnt progress
                    tiqname=get_latest_file(self.par.savedir,extension='tiq')
                    flag=False
                """
            #Stop IQstreaming
            self.rsa.IQSTREAM_Stop()
            time.sleep(self.par.fileInterval)
            self.num += 1

            #END
            nowtimestamp=self.timer.get_now_time_stamp()
            if nowtimestamp>=self.schdule['ENDUnixTime']:
                break

        return self.num









