# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 19:52:12 2018

@author: thomas
"""
from DBmgt import DoSQL

class Get_exinfo():
    
    def __init__(self,connect_db):
        self.connect_db = connect_db
    
    def Get_county_exinfo(self,county_name):
        SQL = "SELECT ex_id,title,county,location,locationName,endTime FROM exinfo WHERE county = %s"
        result,content = DoSQL().S_db(SQL,county_name,2,self.connect_db)
        
        return content
    
    def Get_user_exinfo(self,user_id):
        sql = "select * from exinfo as e1 where exists(select * from user_favorite_exinfo as u1 where u1.ex_id=e1.ex_id and u1.id=%s)"
        result,content=DoSQL().S_db(sql,(user_id),2,self.connect_db)
        return content
    
    def Delete_user_exinfo(self,user_id,delete_exinfo):
        sql = "DELETE FROM user_favorite_exinfo WHERE id=%s and ex_id IN %s"
        DoSQL().IUD_db(sql,(user_id,delete_exinfo),1,self.connect_db)
        
        
