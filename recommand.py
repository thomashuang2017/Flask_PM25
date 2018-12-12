# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 04:22:12 2018

@author: thomas
"""

from PM25 import PM25
from Exinfo import ScrapyExInfo
"""
import exinfo
"""

class recommand():
    
    def recommand_exinfo():
        PM25_min_county = PM25().Get_min_county()
		# -------------------------
		# recommand_county = Get_county_exinfo(PM25_min_county)
		# --------------------------
        recommand_county = ScrapyExInfo.recommand_county_exinfo(PM25_min_county)
        
        return recommand_county
        """
        return exinfo.Get_exinfo(PM25_min_county)
        """
    
        