# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 20:03:38 2018

@author: thomas
"""

from county import county_name
from datetime import datetime
from DBmgt import DoSQL

class Get_PM25():
      
    def __init__(self,connect_db):
        hour = datetime.now().hour + 8
        hour = hour % 9
        cur_pm = 'pm'+ str(hour)
        self.cur_pm = cur_pm
        self.connect_db = connect_db
    
    def Get_PM25(self):
        #hour = datetime.now().hour
        #hour = hour % 9
        SQL = "SELECT county," + self.cur_pm + " FROM PM25 "
        result,content = DoSQL().S_db(SQL,None,2,self.connect_db)
        time = self.cur_pm
        if result == 0:
            return None
        else:
            return content,time
        
    def Get_one_PM25(self,county):
        #hour = datetime.now().hour
        #hour = hour % 9
        SQL = "SELECT county," + self.cur_pm + " FROM PM25 WHERE county = %s"
        result,content = DoSQL().S_db(SQL,county,2,self.connect_db)
        time = self.cur_pm
        if result == 0:
            return None
        else:
            return content,time
    
    def Get_min_county(self):
        
        data,_ = self.Get_PM25()
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
        result,content = DoSQL().S_db(SQL,county,2,self.connect_db)
        
        return content
                
            
        
        
            

        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    