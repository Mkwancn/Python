# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 14:46:50 2020

@author: mkwan
"""

import requests
import json
import jsonpath
import ctypes

if __name__ == "__main__":
    
    Url="https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=8&mkt=zh-CN"
           
    response = requests.get(url=Url).text
    unicodestr = json.loads(response)        
    startdate=jsonpath.jsonpath(unicodestr,'$..startdate')
    url=jsonpath.jsonpath(unicodestr,'$..url')
        
    Url1="https://cn.bing.com"+url[0]      
    content = requests.get(url=Url1)
    
    filepath ="C:/Users/mkwan/Pictures/windows聚焦/"+startdate[0]+".jpg"
    f = open(filepath, "wb")
    f.write(content.content)
    f.close()
    
    ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 0)