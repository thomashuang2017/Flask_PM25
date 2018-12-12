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


#a = exinfo().Get_county_exinfo('宜蘭縣')
#print(a)

#from countyname import county_name


recommand_county = exinfo().Get_county_exinfo('桃園市')
recommand_exinfo = exinfo().Get_county_exinfo(recommand_county)
#a= PM25().Get_past_pm25('桃園市')
#print (a)

#hour = datetime.now().hour
#hour = hour % 9
#cur_pm = 'pm'+ str(hour)
#print(cur_pm)

#a,t = PM25().Get_one_PM25('屏東縣')
#print(a[0][cur_pm])

#print(a)
#b = PM25().Get_min_county()
#print(b[0]['county'])
#print(b)
#ow = IntInterval.closed(0, 35)
#
#county_interval = []
#l
#for i in b:
#    print(i[])
#    single_interval = {}
#    if i['pm3'] in low:
#        single_interval['county'] = i['county']
#        single_interval['interval'] = 0
#    county_interval.append(single_interval)
#    
#print(county_interval)
    #print(i)
        #print(
         #if int(values) in low:
             #print('yes') 
        
#    print(i['county'])
#    print(i['pm3'])
#    print(b[i]['county'])
#    print(b[i]['pm3'])
#a = PM25().Get_county_intervel()
#print(a)



#hour = datetime.now().hour
#hour = hour % 9
#SQL = "SELECT county,pm" + str(hour) + " FROM PM25 "
#result,content = DoSQL().S_db(SQL,None,2)
#
#if result == 0:
#    print('no')
#else:
#    print(content)

#PM25_value = PM25().Get_PM25()
#
#print(PM25_value)
#db  =  pymysql.connect ( host = '35.196.78.102' ,  user = 'root' ,  passwd = "th850413" ,  db = 'flasktest',cursorclass=pymysql.cursors.DictCursor ) 
#cur  =  db.cursor() 
##cur = db.get_db().cursor()
#
## Execute query
#cur.executemany("UPDATE PM25 SET pm=%(pm)s WHERE county=%(county)s",PM25_value) 
#db.commit()
## Commit to DB
##db.connection.commit()
# 
## Close connection
#db.close () 

#print(PM25_value)
#DoSQL().IUD_db("INSERT INTO PM25(county,pm) VALUES(%s, %s)",PM25_value)
#a = PM25.PM25().GetPM25()
#print(a)
