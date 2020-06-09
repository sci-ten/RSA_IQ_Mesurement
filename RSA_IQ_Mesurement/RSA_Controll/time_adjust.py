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
import socket

class TimeAdjust():
    def __init__(self):
        self.call_time=None
        self.recived_time=None
        self.standerd_time=self.set_standerd_time()


    def set_standerd_time(self):
        self.call_time=time.perf_counter()
        #get Time data from NTP in json format
        url = 'https://ntp-a1.nict.go.jp/cgi-bin/json'
        req = urllib.request.Request(url)
        try:
            with urllib.request.urlopen(req,timeout=1) as res:
                body =  json.load(res)
                self.recived_time= time.perf_counter()
                self.standerd_time=body["st"]+(self.recived_time-self.call_time)/2
                print("roundtrip",self.recived_time-self.call_time)
        except:
            print('NTP server time out')
            return None

        return self.standerd_time


    def get_now_time_stamp(self):
        self.now_time=self.standerd_time+time.perf_counter()-self.recived_time
        return self.now_time

class TimeAdjustOffline(TimeAdjust):
    def __init__(self):
        self.standerdtime=self.set_standerd_time()

    def set_standerd_time(self):
        self.standerdtime=time.time()
        return self.standerdtime

    def get_now_time_stamp(self):
        self.now_time=time.time()
        return self.now_time


def convert_datetime(unix):
    date=datetime.datetime.fromtimestamp(unix)
    return date

def convert_string_timestamp_to_milli(dateobj):
    str_time=dateobj.strftime("%Y-%m-%d %H:%M:%S.%f")
    return str_time


def convert_string_timestamp(dateobj):
    str_time=dateobj.strftime("%Y-%m-%d %H:%M:%S")
    return str_time
