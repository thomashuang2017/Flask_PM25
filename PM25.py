# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 20:03:38 2018

@author: thomas
"""

from county import county_name
from intervals import IntInterval
from datetime import datetime
from DBmgt import DoSQL

class PM25():
      
    def __init__(self):
        hour = datetime.now().hour
        hour = hour % 9
        cur_pm = 'pm'+ str(hour)
        self.cur_pm = cur_pm
    
    def Get_PM25(self):
        #hour = datetime.now().hour
        #hour = hour % 9
        SQL = "SELECT county," + self.cur_pm + " FROM PM25 "
        result,content = DoSQL().S_db(SQL,None,2)
        if result == 0:
            return None
        else:
            return content
        
    def Get_one_PM25(self,county):
        #hour = datetime.now().hour
        #hour = hour % 9
        SQL = "SELECT county," + self.cur_pm + " FROM PM25 WHERE county = %s"
        result,content = DoSQL().S_db(SQL,county,2)
        time = self.cur_pm
        if result == 0:
            return None
        else:
            return content,time
       
       
        
    def Get_county_intervel(self):
        
        
        low = IntInterval.closed(0, 35)
        mid = IntInterval.closed(36, 53)
        high = IntInterval.closed(54, 70)
        extr = IntInterval.closed(71,150)
        data = self.Get_PM25()
        
        county_interval = []
        
        for i in data:
            single_interval = {}
            if i[self.cur_pm] in low:
                single_interval['county'] = i['county']
                single_interval['interval'] = 0
            if i[self.cur_pm] in mid:
                single_interval['county'] = i['county']
                single_interval['interval'] = 1
            if i[self.cur_pm] in high:
                single_interval['county'] = i['county']
                single_interval['interval'] = 2
            if i[self.cur_pm] in extr:
                single_interval['county'] = i['county']
                single_interval['interval'] = 3
                
            county_interval.append(single_interval)
                    
        return county_interval
    
    def Get_min_county(self):
        
        data = self.Get_PM25()
        min_pm = 100
        county = ''
        for i in data:
            if i[self.cur_pm] < min_pm:
                min_pm = i[self.cur_pm]
                county = i['county']
        
        return county
    
    
    def predict_PM25():
        
        
        return
    
    def Get_past_pm25(self,county):
        SQL = "SELECT * FROM PM25 WHERE county = %s"
        result,content = DoSQL().S_db(SQL,county,2)
        
        return content
                
            
        
        
            

        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    