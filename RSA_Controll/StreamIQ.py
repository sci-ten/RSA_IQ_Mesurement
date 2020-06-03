'''
Created on 2020/06/02

@author: TUAT
'''
'''
Created on 2019/10/21

@author: TUAT
'''
from ctypes import *
import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import os
import tkinter as tk
import pandas as pd


import csv

from RSA_API import *
from time_adjust import *






# C:\Tektronix\RSA_API\lib\x64 needs to be added to the
# PATH system environment variable
"""################CLASSES AND FUNCTIONS################"""

class Control_RSA:
    """
    Class related to RSA control (IQ streaming)

    Attributes
    ---------
    par : object <class Config_parameter>
        Mesurement parameters
    rsa : object <class 'ctypes.CDLL'>
        RSA api object loaded with ctypes
    """
    def __init__(self,rsa):
        """
        Parameters
        ------------
        rsa: object <class 'ctypes.CDLL'>
            RSA api object loaded with ctypes
        """
        #Create instance for parameter setting
        self.par=Config_parameter()
        #copy to reference rsa object
        self.rsa=rsa

    #config IQ streaming parameter
    def config_iq_stream(self):
        """
        config IQ streaming parameter
        """
        #config file name（time stamp add to end of the file name
        suffixCtl=IQSSDFN_SUFFIX_TIMESTAMP
        dType=IQSOUTDTYPE.IQSODT_INT16
        #config parameter
        self.rsa.CONFIG_SetCenterFreq(c_double(self.par.cf))
        self.rsa.CONFIG_SetReferenceLevel(c_double(self.par.refLevel))
        self.rsa.IQSTREAM_SetAcqBandwidth(c_double(self.par.bw))
        self.rsa.IQSTREAM_SetOutputConfiguration(self.par.dest, dType)
        self.rsa.IQSTREAM_SetDiskFilenameSuffix(suffixCtl)
        self.rsa.IQSTREAM_SetDiskFileLength(c_int(self.par.durationMsec))

        #get sampling rate
        bwActual = c_double(0)
        sampleRate = c_double(0)
        #get sampling rate
        self.rsa.IQSTREAM_GetAcqParameters(byref(bwActual), byref(sampleRate))
        #set samplingrate to Config_parameter
        self.par.set_samplingRate(float(sampleRate.value))

    #Run IQ stream
    def iq_stream(self):
        """
        Run IQ Streaming
        """
        print("###### IQ Stream #####")
        #search device and connect
        Control_RSA.search_connect(self.rsa)
        #setting export type
        self.par.set_dest(IQSOUTDEST.IQSOD_FILE_TIQ)
        #setting measurement parameter to RSA
        self.config_iq_stream()
        #save measuremant parameter
        self.par.export_parameter_csv_with_time()

        timer=TimeAdjust()
        timer.set_standerd_time()
        print("standerdtime",timer.standerd_time)

        ##Run RSA device
        self.rsa.DEVICE_Run()

        self.Streaming_loop_processing(timer)

        print('Streaming finished.')
        iqStreamInfo = IQSTREAM_File_Info()
        self.rsa.IQSTREAM_GetFileInfo(byref(iqStreamInfo))
        Control_RSA.iqstream_status_parser(iqStreamInfo)
        self.rsa.DEVICE_Disconnect()

    def Streaming_loop_processing(self,timer):
        """
        Streaming processing loop part
        """
        num=0
        while True:
            print(num)
            fileName = str(num+1)
            filenameBase = os.path.join(self.par.savedir,fileName)
            self.rsa.IQSTREAM_SetDiskFilenameBase(c_char_p(filenameBase.encode()))
            complete = c_bool(False)
            writing = c_bool(False)
            #Start IQstreaming
            self.rsa.IQSTREAM_Start()


            nowUnixTime=timer.get_now_time_stamp()
            time_file=os.path.join(self.par.savedir,"file_make_time.csv")
            tiqname=str(fileName)

            #add mesuremnt log
            self.add_mesuremnt_log(time_file,nowUnixTime,tiqname)



            #Case of complete.value==False,->continuous mesurement.
            while not complete.value:
                #wait fixed time which is set first.
                time.sleep(self.par.waitTime)
                #Monitor streaming progress.If time passes more than durationMsec,then complete=True.
                self.rsa.IQSTREAM_GetDiskFileWriteStatus(byref(complete), byref(writing))
            #Stop IQstreaming
            self.rsa.IQSTREAM_Stop()
            time.sleep(self.par.fileInterval)
            num += 1


    @staticmethod
    def iqstream_status_parser(iqStreamInfo):
        """
        get state parameter of mesurement

        Paramaters
        ------------
        iqStreamInfo: object <class IQSTREAM_File_Info>
        that is in RSA_API
        """
        # This function parses the IQ streaming status variable
        status = iqStreamInfo.acqStatus
        triggersampleindex = iqStreamInfo.triggerSampleIndex
        triggertimestamp = iqStreamInfo.triggerTimestamp

        if status == 0:
            print('\nNo error.\n')
        if bool(status & 0x10000):  # mask bit 16
            print('\nInput overrange.\n')
        if bool(status & 0x40000):  # mask bit 18
            print('\nInput buffer > 75{} full.\n'.format('%'))
        if bool(status & 0x80000):  # mask bit 19
            print('\nInput buffer overflow. IQStream processing too slow, ',
                  'data loss has occurred.\n')
        if bool(status & 0x100000):  # mask bit 20
            print('\nOutput buffer > 75{} full.\n'.format('%'))
        if bool(status & 0x200000):  # mask bit 21
            print('Output buffer overflow. File writing too slow, ',
                  'data loss has occurred.\n')


    @staticmethod
    def search_connect(rsa):
        """
        Parameters
        ---------------
        rsa: object <class 'ctypes.CDLL'>
            RSA api object loaded with ctypes
        search device and connect
        """
        numFound = c_int(0)
        intArray = c_int * DEVSRCH_MAX_NUM_DEVICES
        deviceIDs = intArray()
        deviceSerial = create_string_buffer(DEVSRCH_SERIAL_MAX_STRLEN)
        deviceType = create_string_buffer(DEVSRCH_TYPE_MAX_STRLEN)
        apiVersion = create_string_buffer(DEVINFO_MAX_STRLEN)

        rsa.DEVICE_GetAPIVersion(apiVersion)
        print('API Version {}'.format(apiVersion.value.decode()))

        Control_RSA.err_check(rsa.DEVICE_Search(byref(numFound), deviceIDs,
                                    deviceSerial, deviceType))

        if numFound.value < 1:
            # rsa.DEVICE_Reset(c_int(0))
            print('No instruments found. Exiting script.')
            exit()
        elif numFound.value == 1:
            print('One device found.')
            print('Device type: {}'.format(deviceType.value.decode()))
            print('Device serial number: {}'.format(deviceSerial.value.decode()))
            Control_RSA.err_check(rsa.DEVICE_Connect(deviceIDs[0]))
        else:
            # corner case
            print('2 or more instruments found. Enumerating instruments, please wait.')
            for inst in deviceIDs:
                rsa.DEVICE_Connect(inst)
                rsa.DEVICE_GetSerialNumber(deviceSerial)
                rsa.DEVICE_GetNomenclature(deviceType)
                print('Device {}'.format(inst))
                print('Device Type: {}'.format(deviceType.value))
                print('Device serial number: {}'.format(deviceSerial.value))
                rsa.DEVICE_Disconnect()
            # note: the API can only currently access one at a time
            selection = 1024
            while (selection > numFound.value - 1) or (selection < 0):
                selection = int(('Select device between 0 and {}\n> '.format(numFound.value - 1)))
            Control_RSA.err_check(rsa.DEVICE_Connect(deviceIDs[selection]))
        rsa.CONFIG_Preset()


    @staticmethod
    def err_check(rs):
        """
        check error number
        Parameters
        -------------
        rs: object
            event RSA API
        """
        if ReturnStatus(rs) != ReturnStatus.noError:
            raise RSAError(ReturnStatus(rs).name)

    @staticmethod
    def add_mesuremnt_log(filepath,nowUnixTime,tiqname):

        #time_str=convert_string_timestamp(nowUnixTime)

        with open(filepath,'a', newline="") as f:
            writer=csv.writer(f)
            writer.writerow([nowUnixTime,tiqname])



class Config_parameter:
    """
    Retain set parameters

    Attributes
    ---------
    cf: float
        center frequency
        [Hz]

    refLevel: float
        reference level
        [dBm]

    bw: float
        bandwidth
        [Hz]

    durationMsec: int
        Continuous observation time (cycle) Time to stream to one file
        [usec]

    waitTime: float
        Cycle to confirm the end of streaming of one file
        [sec]

    fileInterval: float
        File make interval.Make each tiq files after wating for the value.
        [sec]

    __samplingRate: float
        sampling rate (private variable)
        [Hz]

    savedir: string
        tiq file save directory

    dest: object <class 'ctypes.c_long'>
        setting export type
    """

    def __init__(self):
        #set measurement parameters
        #center freqency[Hz]
        self.cf=0.0
        #reference level [dBm]
        self.refLevel=-30
        #band width [Hz]
        self.bw=0.0
        #Continuous observation time (cycle) Time to stream to one file [usec]
        self.durationMsec=0
        #Cycle to confirm the end of streaming of one file
        self.waitTime=0
        #File make interval.Make each tiq files after wating for the value[sec]
        self.fileInterval=0.0
        #samping rate (private variable)
        self.__samplingRate=0.0
        #save file directory
        self.savedir=None
        #the output data destination and IQdatatype.
        self.dest=None


    def set_parameter(self,cf,refLevel,bw,durationMsec,waitTime,fileInterval,savedir):
        """
        set measurement parameter

        Parameters
        ---------------
        cf: float
        center frequency
        [Hz]

        refLevel: float
            reference level
            [dBm]

        bw: float
            bandwidth
            [Hz]

        durationMsec: int
            Continuous observation time (cycle) Time to stream to one file
            [usec]

        waitTime: float
            Cycle to confirm the end of streaming of one file
            [sec]

        fileInterval: float
            File make interval.Make each tiq files after wating for the value
            [sec]

        savedir: string
            save directory tiq file
        """
        self.cf=cf
        self.refLevel=refLevel
        self.bw=bw
        self.durationMsec=durationMsec
        self.waitTime=waitTime
        self.fileInterval=fileInterval
        self.savedir=savedir

    #Check parameters are set properly
    def check_parameter(self):
        """
        Check parameters are set properly
        """
        try:
            self.cf=float(self.cf)
            self.refLevel=float(self.refLevel)
            self.bw=float(self.bw)
            self.durationMsec=int(self.durationMsec)
            self.waitTime=float(self.waitTime)
            self.fileInterval=float(self.fileInterval)

        except:
            print("The parameter is not set properly.")
            return False

        try:
            if not os.path.exists(self.savedir):
                print("save directory not exsists.")
                return False
        except:
            print("save path is not set properly.")
            return False


        return True

    #getter to samplingRate
    def get_samplingRate(self):
        """
        getter to samplingRate
        """
        return self.__samplingRate

    def set_samplingRate(self,samplingRate):
        """
        setter to samplingRate
        """
        self.__samplingRate=samplingRate


    def set_dest(self,dest):
        self.dest=dest

    def print_prameter(self):
        """
        print parameter to console
        """
        print("### 観測パラメータ###")
        print("Center Freqency[Hz]",self.cf)
        print("Reference Level[dBm]",self.refLevel)
        print("Band Width[Hz]",self.bw)
        print("Duration[msec]",self.durationMsec)
        print("Wait Time[sec]",self.waitTime)
        print("Make File Interval [sec]",self.fileInterval)
        print("Save Directory",self.savedir)

    def export_parameter_csv_with_time(self):
        filename="measurement_parameter.csv"
        samplingRate=self.get_samplingRate()
        df=pd.DataFrame([["Center Freqency[Hz]",self.cf],
                         ["Reference Level[dBm]",self.refLevel],
                         ["Band Width[Hz]",self.bw],
                         ["Sampling Rate[Hz]",samplingRate],
                         ["Duration[msec]",self.durationMsec],
                         ["Wait Time[sec]",self.waitTime],
                         ["Make File Interval [sec]",self.fileInterval]
                         ]
                        ,columns=['parameter', 'value']
                        )
        df.to_csv(os.path.join(self.savedir,filename))


def main():
    #set the RSA API path
    os.chdir("C:\\Tektronix\\RSA_API\\lib\\x64")
    rsa = cdll.LoadLibrary("RSA_API.dll")
    #control RSA
    mang_rsa=Control_RSA(rsa)
    #GUI
    win = tk.Tk()
    app = GuiApp.GUI_App(master=win,mang_rsa=mang_rsa)
    #run gui application
    app.mainloop()

if __name__ == '__main__':
    main()