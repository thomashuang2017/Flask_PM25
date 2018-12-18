# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 19:52:12 2018

@author: thomas
"""
from DBmgt import DoSQL

class exinfo():
    
    def __init__(self,connect_db):
        self.connect_db = connect_db
    
    def Get_county_exinfo(self,county_name):
        SQL = "SELECT ex_id,title,county,location,locationName,endTime FROM exinfo WHERE county = %s"
        result,content = DoSQL().S_db(SQL,county_name,2,self.connect_db)
        
        return content
