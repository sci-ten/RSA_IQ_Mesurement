'''
Created on 2020/06/06

@author: HIROTO
'''

import pandas as pd

def read_parameter_csv(path):
    df=pd.read_csv(path, header=0,index_col=0)

    return df
