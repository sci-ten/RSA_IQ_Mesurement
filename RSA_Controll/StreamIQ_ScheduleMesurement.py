'''
Created on 2020/06/05

@author: HIROTO
'''

from RSA_Controll.StreamIQ import *

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

    def set_timer(self,timer):
        self.timer=timer

    def iq_stream(self):
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
        self.par.export_parameter_csv_with_time()

        ##Run RSA device
        self.rsa.DEVICE_Run()






