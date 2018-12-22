# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 00:10:05 2018

@author: thomas
"""

import requests
from county import county_name
import csv
from DBmgt import DoSQL
import time
from datetime import datetime

def scrap_PM25_toDB():
    # DownloadPM25 to dict
    CSV_URL = 'https://opendata.epa.gov.tw/ws/Data/ATM00625/?$format=csv'
    download = requests.get(CSV_URL,verify=False)
    download = download.content.decode("utf-8")
    reader = csv.reader(download.split('\n'), delimiter=',')
        
    
    data = []
    for row in reader:
        data.append(row)
        
    county_pm25 = []    
    
    for i in range(0,len(county_name)):
        num_pm25 = []
        pm = {}
        for j in range(1,len(data)-1):
            if county_name[i] == data[j][1]:
                if data[j][2] != '':
                    num_pm25.append(int(data[j][2]))
        
        pm['county'] = county_name[i]
        if not num_pm25:
            pm['pm'] = 0
        else:
            pm['pm'] = max(num_pm25)
            county_pm25.append(pm)
        
    return county_pm25
#result,data = DoSQL().S_db("SELECT title FROM PM25",'',1)
    
#DoSQL().IUD_db("INSERT INTO PM25(county,pm1) VALUES(%s, %s, %s)",(username,email,password),1)
    
    #DoSQL().IUD_db("UPDATE PM25 SET pm=%(pm)s WHERE county=%(county)s",county_pm25,2)
    
    
    
if __name__ == '__main__':
    
    while True:
        
        # connect_db
        connect_db = DoSQL().get_conn()
    
        
        hour = datetime.now().hour # 現在時間
        county_pm25 = scrap_PM25_toDB() #爬 pm25
        result,data = DoSQL().S_db("SELECT county FROM PM25",None,2,connect_db) #確認table是否為空
        
        hour = hour%9 # 9小時統計 ex 13:00 % 9 = 4
        
        if result == 0:
            SQL = "INSERT INTO PM25(county,pm" + str(hour) + ") VALUES(%(county)s, %(pm)s)"
            DoSQL().IUD_db(SQL,county_pm25,2,connect_db)
        else:
            SQL = 'UPDATE PM25 SET pm' + str(hour) + '=%(pm)s WHERE county=%(county)s'
            DoSQL().IUD_db(SQL,county_pm25,2,connect_db)
            
        DoSQL().close_conn(connect_db)
        
        time.sleep(3600)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        

