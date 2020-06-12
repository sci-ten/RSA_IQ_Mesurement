'''
Created on 2020/06/06

@author: HIROTO
'''

class LocalBackUp():
    """
    Create backup file which store data to be uploaded to the database
    ,as csv.

    Attributes
    -----------------
    savedir
    """
    def __init__(self,savedir):
        self.savedir=savedir

    def save(self,df):
        df.to_csv(self.savedir+'//log.csv')


