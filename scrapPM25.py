# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 00:10:05 2018

@author: thomas
"""

import requests
from county import county_name
import csv
from DBmgt import DoSQL
from datetime import datetime
from config import config


class scrapPM25():
    def scrap_PM25_toDB(self):
        # DownloadPM25 to dict
        CSV_URL = 'https://opendata.epa.gov.tw/ws/Data/ATM00625/?$format=csv'
        download = requests.get(CSV_URL,verify=False)
        download = download.content.decode("utf-8")
        reader = csv.reader(download.split('\n'), delimiter=',')
            
        
        data = []
        for row in reader:
            data.append(row)
            
        county_pm25 = []    
        
        now_time = datetime.now(config['GetlocaltimeConfig'].tz).strftime("%Y-%m-%d %H:%M:%S")
        
        
        for i in range(0,len(county_name)):
            num_pm25 = []
            pm = {}
            for j in range(1,len(data)-1):
                if county_name[i] == data[j][1]:
                    if data[j][2] != '':
                        num_pm25.append(int(data[j][2]))
            
            pm['time'] = str(now_time)
            pm['county'] = county_name[i]
            if not num_pm25:
                pm['pm'] = 0
            else:
                pm['pm'] = max(num_pm25)
                county_pm25.append(pm)
        
        # connect_db
        connect_db = DoSQL().get_conn()
        
        #county_pm25 = scrap_PM25_toDB() #爬 pm25
        result,data = DoSQL().S_db("SELECT county FROM PM25",None,2,connect_db) #確認table是否為空
 
        hour = datetime.now(config['GetlocaltimeConfig'].tz).hour
        
       
        
        
        
        hour = hour%9 # 9小時統計 ex 13:00 % 9 = 4
        
        if result == 0:
            SQL = "INSERT INTO PM25(county,pm" + str(hour) + ",c_time) VALUES(%(county)s, %(pm)s ,%(time)s)"
            #SQL = "INSERT INTO PM25(county,pm" + str(hour) + ",current_time) VALUES(%(county)s, %(pm)s ,%(current_time)s)"
            DoSQL().IUD_db(SQL,county_pm25,2,connect_db)
                       
        else:
            SQL = 'UPDATE PM25 SET pm' + str(hour) + '=%(pm)s,c_time=%(time)s WHERE county=%(county)s'
            #SQL = "UPDATE PM25 SET pm" + str(hour) + "=%(pm)s,current_time=%(current_time)s  WHERE county=%(county)s"
            DoSQL().IUD_db(SQL,county_pm25,2,connect_db)
            
            
            
        #DoSQL().close_conn(connect_db)



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        

