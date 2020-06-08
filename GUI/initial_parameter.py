'''
Created on 2020/06/02

@author: HIROTO
'''
import os
import pickle

class Initial_Parameters:
    """
    Class for setting initial values ​​of mesurement parameters.
    Summarize file processing etc. to set the parameters used in the previous observation.
    """
    def __init__(self):
        #default last mesurement parameter save path
        self.spath=r"C:\pleiades\workspace\RSA_IQ_STREAMING\last_parameters.pickle"

    def set_savepath(self,spath):
        """
        set a save path for last mesurement parameters

        Parameters
        ------------------
        spath: String
            set a save path for last mesurement parameters
        """
        self.spath=spath

    def make_dic(self,cf,refLevel,bw,durationMsec,fileInterval):
        """
        Paramaters
        -----------
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

        fileInterval: float
            File make interval.Make each tiq files after wating for the value
            [sec]

        Returns
        ----------
        dic_par: dictionary
            mesurement parameters
        """

        dic_par={"Center Freqency":cf,
                 "Reference Level":refLevel,
                 "Band Width":bw,
                 "Duration":durationMsec,
                 "Make File Interval":fileInterval}
        return dic_par


    def load_parameter(self):
        """
        Load observation parameter dictionary object in pickle format.
        if file is not found then Returns the initial value of the default parameter.

        Returns
        ------------
        dic_par: dictionary
            mesurement parameters
        """
        if os.path.exists(self.spath):
            print("last parameters file exsists")
            with open(self.spath,mode='rb') as f:
                dic_par=pickle.load(f)
            print(dic_par)
        else:

            dic_par={"Center Freqency":2437.0,
                 "Reference Level":-30,
                 "Band Width":1.25e6,
                 "Duration":1000,
                 "Make File Interval":0.0}

        return dic_par


    def save_parameter(self,dic_par):
        """
        Save observation parameter dictionary object in pickle format

        Parameters
        ------------
        dic_par: dictionary
            mesurement parameters
        """
        with open(self.spath,mode='wb') as f:
            pickle.dump(dic_par,f)
