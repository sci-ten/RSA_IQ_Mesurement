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
    def __init__(self,parameter,timer):
        """
        parameter: dictionary
            mesurement parameter
        """
        os.chdir("C:\\Tektronix\\RSA_API\\lib\\x64")
        rsa = cdll.LoadLibrary("RSA_API.dll")

        self.mang_rsa=Control_RSA(rsa=rsa,timer=timer)
        self.conf=self.mang_rsa.par
        self.app_state=False

        #Set parameter
        self.conf.set_parameter(cf=parameter['cf'],refLevel=parameter['refLevel'],bw=parameter['bw'],durationMsec=parameter['durationMsec'],fileInterval=parameter['fileInterval'],savedir=parameter['savedir'])

    def Run(self):
        if self.app_state==True:
            self.conf.print_prameter()
            #Start IQ Streaming
            self.mang_rsa.iq_stream()

    def RunCheck(self):
        self.app_state=self.conf.check_parameter()
        return self.app_state
