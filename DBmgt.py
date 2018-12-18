# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 16:34:09 2018

@author: gaga
"""

import pymysql


    
config = {
          'host':'35.196.78.102',
          'user':'root',
          'password':'th850413',
          'db':'flasktest',
          'cursorclass':pymysql.cursors.DictCursor,
          }
    


class DoSQL():

    
    def get_conn(self):
        conn = pymysql.connect(**config)
     
     
        return conn
    
    def close_conn(self,connect):
        connect.close()
    
    
    def S_db(self,sql,params,fetch,conn):
        
        db = conn
        #db  =  pymysql.connect (**config) 
        
        cur  =  db.cursor()  
        
        # Get
        result = cur.execute(sql,(params))
    
        # fetch one or all
        if fetch == 1:
            content = cur.fetchone()
        else:
            content = cur.fetchall()
            
        #close cursor 
        #content = list(content)

        return result,content
    
    # Insert , Update , Delete
    def IUD_db(self,sql,params,ex):
        
        # Create cursor
        #cur = db.connection.cursor()
        
        db  =  pymysql.connect (**config) 
        cur  =  db.cursor() 
        #cur = db.get_db().cursor()
        
        # Execute query
        if ex == 1:
            cur.execute(sql,(params)) 
        else:
            cur.executemany(sql,(params)) 
        db.commit()
        
        db.close () 


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    