# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 22:02:53 2018

@author: thomas
"""

from PM25 import PM25
from DBmgt import DoSQL
import json
import pymysql
from datetime import datetime
from intervals import IntInterval
from exinfo import exinfo
from scrapPM25 import scrap_PM25_toDB

import requests
import csv


county_pm,time = PM25().Get_one_PM25('南投縣')
print(county_pm)
print(time)
print(county_pm[0][time])
#county_pm25 = scrap_PM25_toDB()
#min_county = PM25().Get_min_county()
#county_name = ['南投縣',
# '嘉義市',
# '嘉義縣',
# '基隆市',
# '宜蘭縣',
# '屏東縣',
# '彰化縣',
# '新北市',
# '新竹市',
# '新竹縣',
# '桃園市',
# '澎湖縣',
# '臺中市',
# '臺北市',
# '臺南市',
# '臺東縣',
# '花蓮縣',
# '苗栗縣',
# '連江縣',
# '金門縣',
# '雲林縣',
# '高雄市']
#
#
#CSV_URL = 'https://opendata.epa.gov.tw/ws/Data/ATM00625/?$format=csv'
#download = requests.get(CSV_URL,verify=False)
#download = download.content.decode("utf-8")
#reader = csv.reader(download.split('\n'), delimiter=',')
#    
#
#data = []
#for row in reader:
#    data.append(row)
#    
#county_pm25 = []    
#
#for i in range(0,len(county_name)):
#    num_pm25 = []
#    pm = {}
#    for j in range(1,len(data)-1):
#        if county_name[i] == data[j][1]:
#            if data[j][2] != '':
#                num_pm25.append(int(data[j][2]))
#    
#    pm['county'] = county_name[i]
#    if not num_pm25:
#        pm['pm'] = 0
#    else:
#        pm['pm'] = max(num_pm25)
#        county_pm25.append(pm)
#        
#        
#print(type(county_pm25[0]['pm']))     
#        
#        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

