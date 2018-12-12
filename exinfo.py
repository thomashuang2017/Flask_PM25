# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 19:52:12 2018

@author: thomas
"""
from DBmgt import DoSQL

class exinfo():
    
    def Get_county_exinfo(self,county_name):
        SQL = "SELECT title,county,location,locationName,endTime FROM exinfo WHERE county = %s"
        result,content = DoSQL().S_db(SQL,county_name,2)
        
        return content        return content
    #def Get_county_exinfo(county_name):
    #    sql = "SELECT * FROM EXINFO WHERE COUNTY = %s"
    #    Get_county_exinfo = DoSQL().S_db(sql,county_name)
    #    
    #    return Get_county_exinfo
        
    def recommand_county_exinfo(PM25_min_county):
        sql = "SELECT TITLE,LOCATION,LOCATIONNAME,ENDTIME FROM EXINFO WHERE COUNTY = %S"
        recommand_county_exinfo = DoSQL().S_db(sql,PM25_min_county)
        
        return recommand_county_exinfo