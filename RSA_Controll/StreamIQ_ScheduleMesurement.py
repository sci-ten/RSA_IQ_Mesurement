'''
Created on 2020/06/05

@author: HIROTO
'''

from RSA_Controll.StreamIQ import *
from RSA_Controll.time_adjust import *
from RSA_Controll.Mesurement_log import *
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
        super().__init__(rsa)
        self.timer=timer
        self.timedic={'StartTimeStamp':None,'StartUnixTime':None,'EndTimeStamp':None,'ENDUnixTime':None}
        self.num=0

    def set_timer(self,timer):
        self.timer=timer

    def iq_stream(self,id,schdule):
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

        #save measuremant parameter
        #self.par.export_parameter_csv_with_time()

        self.id=id
        self.schdule=schdule

        ##Run RSA device
        self.rsa.DEVICE_Run()

        #get_now_time_stamp
        self.timedic['StartUnixTime']=self.timer.get_now_time_stamp()
        self.timedic['StartTimeStamp']=convert_string_timestamp(self.timedic['StartUnixTime'])

        #IQ streaming Loop part
        self.Streaming_loop_processing()

        self.timedic['ENDUnixTime']=self.timer.get_now_time_stamp()
        self.timedic['EndTimeStamp']=convert_string_timestamp(self.timedic['ENDUnixTime'])

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

            #add mesuremnt log
            prog=MesurementProgress(self.par.savedir)
            nowUnixTime=self.timer.get_now_time_stamp()
            tiqname=str(fileName)
            prog.add_mesuremnt_log(nowUnixTime,tiqname)

            #Case of complete.value==False,->continuous mesurement.
            while not complete.value:
                #Monitor streaming progress.If time passes more than durationMsec,then complete=True.
                self.rsa.IQSTREAM_GetDiskFileWriteStatus(byref(complete), byref(writing))

            #Stop IQstreaming
            self.rsa.IQSTREAM_Stop()
            time.sleep(self.par.fileInterval)
            self.num += 1

            #END
            time=self.timer.get_now_time_stamp()
            if time >=self.schdule['ENDUnixTime']:
                break

        return self.num









