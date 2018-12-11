# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 19:54:09 2018

@author: thomas
"""

import requests
import json
from DBmgt import DoSQL

# ------- scrapy exinfo-----------------


json_url = 'https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJ&category=6'
download = requests.get(json_url,verify=False)
download = download.content.decode("utf-8")
j = json.loads(download)
show = []
for i in range(0,len(j)):
    show.append({'title': j[i]['title'],
    'location':j[i]['showInfo'][0]['location'],
    'locationName':j[i]['showInfo'][0]['locationName'],
    'endTime':j[i]['showInfo'][0]['endTime'][:10],
    'county':j[i]['showInfo'][0]['location'][:3]})
    
# ----------Do SQL--------------------
    
SQL = "INSERT INTO exinfo(title,county,location,locationName,endTime) VALUES(%(title)s, %(county)s, %(location)s, %(locationName)s, %(endTime)s)"
DoSQL().IUD_db(SQL,show,2)