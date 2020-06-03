'''
Created on 2020/06/03

@author: TUAT
'''
'''
Created on 2020/05/28

@author: HIROTO
'''
#Standard library
import json
import time
import urllib.request
import datetime
import sched


class TimeAdjust():
    def __init__(self):
        self.call_time=None
        self.recived_time=None
        self.standerd_time=None


    def set_standerd_time(self):
        self.call_time=time.perf_counter()
        #get Time data from NTP in json format
        url = 'https://ntp-a1.nict.go.jp/cgi-bin/json'
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as res:
            body =  json.load(res)
            self.recived_time= time.perf_counter()
            self.standerd_time=body["st"]+(self.call_time-self.recived_time)/2

        return self.standerd_time


    def get_now_time_stamp(self):
        self.now_time=self.standerd_time+time.perf_counter()-self.recived_time
        return self.now_time

def convert_string_timestamp(unixtime):
    mili=unixtime.microsecond[:4]
    mu=unixtime.microsecond[3:]


    str_time=str(unixtime.year)+'/'+str(unixtime.day) \
    +'/'+str(unixtime.month)+' '+str(unixtime.minute)+str(unixtime.second) \
    +':'+mili+':'+mu

    return str_time

"""
x=TimeAdjust()
x.set_standerd_time()
x.get_now_time_stamp()
print(x.get_now_time_stamp())
print(x.standerd_time)

"""