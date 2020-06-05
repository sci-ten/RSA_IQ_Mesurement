'''
Created on 2020/06/05

@author: HIROTO
'''

import os
import tkinter as tk
from ctypes import *

from RSA_Controll.StreamIQ import *


class SimpleSettingMode():
    """
    Execute IQ Streaming with parameters read from GUI in simple setting mode

    Attributes
    -------------------
    mang_rsa: object <class Control_RSA>
        object to control RSA
    conf: object <class Config_parameter>
    app_state : bool
        Whether the parameters are set correctly.
    """
    def __init__(self,parameter):
        """
        parameter: dictionary
            mesurement parameter
        """
        os.chdir("C:\\Tektronix\\RSA_API\\lib\\x64")
        rsa = cdll.LoadLibrary("RSA_API.dll")

        self.mang_rsa=Control_RSA(rsa=rsa)
        self.conf=self.mang_rsa.par

        #Set parameter
        self.conf.set_parameter(cf=parameter['cf'],refLevel=parameter['refLevel'],bw=parameter['bw'],durationMsec=parameter['durationMsec'],waitTime=parameter['waitTime'],fileInterval=parameter['fileInterval'],savedir=parameter['savedir'])

    def Run(self):
        #RUN
        if self.app_state:
            self.conf.print_prameter()
            #Start IQ Streaming
            self.mang_rsa.iq_stream()
        else:
            print("Please try again setting")
            return

    def RunCheck(self):
        self.app_state=self.conf.check_parameter()
        if not self.app_state:
            return False
        return True
