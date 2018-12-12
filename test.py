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


county_pm25 = scrap_PM25_toDB()


