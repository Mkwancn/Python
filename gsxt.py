# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 09:16:36 2020

@author: mkwan
"""

#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
'''通过国家企业信用信息公示系统(www.gsxt.gov.cn) Mobile App HTTP API 查询企业信息'''

import json
import requests
from urllib import parse
import jsonpath
import time

URL = 'http://app.gsxt.gov.cn/gsxt/cn/gov/saic/web/controller/PrimaryInfoIndexAppController/search?page=1'
USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0'
ACCEPT_LANGUAGE = 'zh-CN'
ACCEPT_ENCODING = 'gzip,deflate'
XRW = 'XMLHttpRequest'
CHARSET = 'application/json;charset=utf-8'


def query(keyword):
    '''main entry'''
    quoted = parse.quote(keyword)
    _data = {'searchword':quoted,
             'conditions':{"excep_tab":"0","ill_tab":"0","area":"0","cStatus":"0","xzxk":"0","xzcf":"0","dydj":"0"},
             'sourceType': 'I'}
    _data=json.dumps(_data)
    '''requests发送请求的data需要是str格式，写的是json格式，也就是Python里的dict,需要转换才能用，但是如果只看报错504，根本不知道是什么原因'''
    new_data = json.loads(_data)
    _headers = {
                'Host': 'app.gsxt.gov.cn',
                'Content-Type': CHARSET,
                'Cookie':'JSESSIONID=ED93DD9095E84CF9A83AF8D37E8BDCDF; SECTOKEN=7399816924015363605; __jsluid_h=e5db740b32297dcbdd76bf38847653be; tlb_cookie=172.16.12.1068080',
                'Accept': 'application/json',
                'User-Agent': USER_AGENT,
                'Accept-Language': ACCEPT_LANGUAGE,
                'X-Requested-With': XRW
                }

    _response = requests.post(URL, json=new_data, headers=_headers)
    
    while(_response.status_code!=200):
        if(_response.status_code==403):
            print(_response.status_code)
            return
        print(_response.status_code)
        _response = requests.post(URL, json=new_data, headers=_headers)
        time.sleep(2)
    '''print(_response.json())'''
    _content = _response.json()
    data=jsonpath.jsonpath(_content,'$..pripid')
    if data:
        return data[0]
    else:
        return

def query2(keyword,enter,keyword1):
    url='http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-'+keyword+'-'+enter+'.html?'
    hea = {
                'Host': 'app.gsxt.gov.cn',
                'Origin':'null',
                'Cookie':'JSESSIONID=ED93DD9095E84CF9A83AF8D37E8BDCDF; SECTOKEN=7399816924015363605; __jsluid_h=e5db740b32297dcbdd76bf38847653be; tlb_cookie=172.16.12.1068080',
                'User-Agent': USER_AGENT,
                'Accept-Language': ACCEPT_LANGUAGE,
    }
    dat={'nodeNum':'110000',
         'entType':'10',
         'start':'0',
         'sourceType':'I'
            }
    response=requests.post(url,data=dat,headers=hea)
    while(response.status_code!=200):
        if(response.status_code==403):
            print(response.status_code)
            return
        print(response.status_code)
        response=requests.post(url,data=dat,headers=hea)
        time.sleep(2)
    '''print(response.status_code)'''
    return response.json()

if __name__ == "__main__":
    dic={}
    
    with open('org_name.json','r',encoding='utf8')as fp:
        json_data = json.load(fp)
    with open('arri.json','r',encoding='utf8')as fp3:
        json_data1 = json.load(fp3)
    
    for keyword in json_data:
        dic1={keyword:query(keyword)
                }
        dic.update(dic1)
        dic2={}
        if dic1.get(keyword):
            for keyword1 in json_data1:                
                dic3={keyword1:query2(keyword1,dic1.get(keyword),keyword)
                }
                dic2.update(dic3)
        time.sleep(1)
        with open('enterprise.json', 'a') as fp:
            dic5={keyword:dic2
                    }
            json.dump(dic5,fp=fp,indent=2, sort_keys=True, ensure_ascii=False)
            fp.write('\r\n')
            
    print('Finish')
    with open('eachenter.json', 'w') as fp1:
        json.dump(dic,indent=4,fp=fp1,sort_keys=True,ensure_ascii=False)