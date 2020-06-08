'''
Created on 2020/06/06

@author: HIROTO
'''
#import traceback
import pandas as pd

import pymysql
import sqlalchemy as sqa


class DBinfo():
    """
    This class has sign in information to database.

    Attributes
    ---------------
    dic : dictionary
        Database login information such as "UserName","HostName","Password","DatabaseName"
    flag : bool
        flag of whether connected database
    """
    def __init__(self):
        self.dic={"UserName":None,"HostName":None,"Password":None,"DatabaseName":None}
        self.flag=False

    def flag_on(self):
        self.flag=True

class ConnectDB():
    """
    connect MySQL Data baseb using pymysql and sqlalchemy

    Attrubutes
    ---------------
    user : String

    host : String
        SQL server name or IP address (e.g. "192.168.1.1"

    password : String
        Sign in password

    dBName : String
        Database which you use

    url : Striing
        url to create engine of sqlalchemy

    engine : String
        engine object of sqlalchemy,used for upload data to SQL server.
    """
    def __init__(self,DB_dic):
        """
        Parameters
        ------------
        DB_dic : dictionary
            Database login information such as "UserName","HostName","Password","DatabaseName"
        """
        self.user=DB_dic["UserName"]
        self.host=DB_dic["HostName"]
        self.password=DB_dic["Password"]
        self.dbName=DB_dic["DatabaseName"]
        self.url=self.make_url()
        self.engine= sqa.create_engine(self.url, echo=False)

        #connect my sql, Returns True if successful
        self.result=self.connect_mysql()


    def connect_mysql(self):
        try:
            self.conn= pymysql.connect(
            user=self.user,
            passwd=self.password,
            host=self.host,
            )
            self.cur=self.conn.cursor()
            return True

        except pymysql.err.OperationalError:
            return False

    def use_db(self):
        query="USE "+str(self.dBName)+";"
        self.cur.execute(query)

    def make_url(self):
        self.url='mysql+pymysql://%s:%s@%s/%s?charset=utf8' %(self.user,self.__password,self.host,self.dbName)
        return self.url


class MesurementParmsTable():
    def __init__(self):
        self.ms_parms_df=pd.DataFrame(columns=['id','StartTime','StartUnixTime','EndTime','EndUnixTime','TIQDir'\
                                               ,'TIQnum','CenterFrequency','BandWidth','RefLevel','Duration','FileMakeInterval'\
                                               ,'MesurementMode','Tag','Location','Description'])

    def marge_ex_data_as_dfSeries(self,id,time_dic,path,TIQnum,param,ms_mode,tag=None,location=None,Description=None):
        samplingrate=param.get_samplingRate()

        Series=pd.Series([id,time_dic['StartTime'],time_dic['StartUnixTime'],time_dic['EndTime'],time_dic['EndUnixTime']\
                          ,path,TIQnum,param.cf,param.bw,param.refLevel,param.durationMsec,param.fileInterval,\
                          ms_mode,tag,location,Description],index=self.ms_parms_df.columns)

        return Series

    def append_dfSeries(self,series):
        self.ms_parms_df=self.ms_parms_df.append(series, ignore_index=True)

class UpdateMesurementParms():
    def __init__(self,engine):
        self.engine=engine

    def update_for_db(self,ms_params_Series):
        #convert pandas Series to pandas dataframe to use to_sql method
        ms_params=pd.DataFrame([ms_params_Series])
        ms_params.to_sql('df', self.engine, index=False, if_exists='append')

