# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 18:28:25 2018

@author: thomas
"""

import pytz
import pymysql

class GetlocaltimeConfig:
    tz = pytz.timezone('Asia/Taipei')

class ScrapPM25Config:
    
    JOBS = [
        {
            'id': '111',              # 不重複的標識
            'func': '__main__:job_1',  # 定時執行的 模組：函式
            'trigger': 'interval',         # 定時執行，其他可選引數data,interval
            'seconds':5
            
        
        }
    ]

    
class DBConfig:
    
    connect_dict = {
          'host':'35.221.254.37',
          'user':'lifebear',
          'password':'th850413',
          'db':'flasktest',
          'cursorclass':pymysql.cursors.DictCursor,
          }    



config = {
        
'ScrapPM25Config':ScrapPM25Config,
'GetlocaltimeConfig':GetlocaltimeConfig,
'DBConfig':DBConfig

}