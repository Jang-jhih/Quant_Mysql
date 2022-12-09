#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 18:13:23 2022

@author: jacob
"""
import http.cookiejar
import ssl
import requests
import pandas as pd
import os
import time
import random
from fake_useragent import UserAgent

# import sqlite3
import datetime
import urllib.request
import warnings
warnings.filterwarnings("ignore")
from Crawler.Stock import *
# import os
import pickle
date_range_record_file = os.path.join('history', 'date_range.pickle')
# import sqlalchemy
# import datetime
# import os
# import pandas as pd




def Crawler_IP():
    response = requests.get("https://www.sslproxies.org/")
    proxy_ips = re.findall('\d+\.\d+\.\d+\.\d+:\d+', response.text)  #「\d+」代表數字一個位數以上

    valid_ips = []
    for ip in proxy_ips:
        try:
            result = requests.get('https://ip.seeip.org/jsonip?',proxies={'https': ip,'http': ip},timeout=60)
            print(result.json())
            valid_ips.append(ip)
        except:
            print(f"{ip} invalid")
    

    df = pd.DataFrame({'proxy_ips':valid_ips})
    # df = pd.DataFrame({'proxy_ips':proxy_ips})
    
    df = df.drop_duplicates() 
    df['date'] = datetime.datetime.now()
    # add_to_csv('proxy_ips',df)

    save = to_CSV(table_name = 'proxy_ips',platform='tool')
    save.add_to_csv(new_df=df,TimeColumn='date')


def get_requests(url,SSL=True):
    ua = UserAgent()
    headers = {'user-agent' : ua.google}
    
    check=0
    while check==0:
        IPfile = pd.read_csv(os.path.join('Datasource','tool','proxy_ips.csv'))
        if len(list(IPfile['proxy_ips']))<3:
            Crawler_IP()
        ip = random.choice(list(IPfile['proxy_ips']))
        print(ip)
        try:
            if SSL == True:

                time.sleep(3)
                context = ssl._create_unverified_context()
                res = urllib.request.Request(url,headers=headers) # 發送請求
            #%%建立Cookie
                cjar = http.cookiejar.CookieJar()
                cookie = urllib.request.HTTPCookieProcessor(cjar)
            #%%建立url
                if len(list(IPfile['proxy_ips']))<3:
                    Crawler_IP()
                ip = random.choice(list(IPfile['proxy_ips']))
                print(ip)
                proxy = urllib.request.ProxyHandler({"https": ip})
                opener = urllib.request.build_opener(cookie,proxy)
                urllib.request.install_opener(opener)
                res = urllib.request.urlopen(res,context=context).read() #讀取Http
                return res
                check=1
            else:
                ses = requests.Session()
                response = ses.get(url=url, headers=headers,proxies={'https': ip,'http': ip}, timeout = 5000)
                time.sleep(3)
                check=1
                return response
        except:
            print(f'{ip} 已經失效，即將剃除後重新選擇IP')
            proxy_ips = IPfile[IPfile['proxy_ips'] != ip]
            proxy_ips.to_csv(os.path.join('Datasource','tool','proxy_ips.csv'), index = False)
    


class to_CSV:

    def __init__(self,table_name,platform):
        self.table_name=table_name
        self.platform=platform
        
        if not os.path.isdir('Datasource'):
            os.mkdir('Datasource')
            
        if not os.path.isdir(os.path.join('Datasource',platform)):
            os.mkdir(os.path.join('Datasource',platform))

    def add_to_csv(self,new_df,TimeColumn):
        table_name = self.table_name
        platform = self.platform

        old_file_name = os.path.join('datasource',platform,table_name+'.csv')
        TMP_file_name = os.path.join('datasource',platform,f'TMP{table_name}.csv')
            
        if os.path.isfile(old_file_name):
            old_file = pd.read_csv(old_file_name)
            old_file[TimeColumn] = pd.to_datetime (old_file[TimeColumn])

            old_file = pd.concat([old_file,new_df])

            old_file.drop_duplicates(inplace = True)

            old_file.to_csv(TMP_file_name,encoding = 'utf-8-sig',index = False)
    
            os.remove(old_file_name)
            os.rename(TMP_file_name,old_file_name)

        else:
            new_df[TimeColumn] = pd.to_datetime (new_df[TimeColumn])
            new_df.to_csv(old_file_name,encoding = 'utf-8-sig',index = False) 


    def latest_data(self,key):
        table_name = self.table_name
        platform = self.platform
        maindirectory = os.path.join('Datasource',platform)
        List = list(pd.read_csv(os.path.join(maindirectory,f'{table_name}.csv'))[key])
        return List[-1]




#%%


def table_date_range(table_name):
    global date_range_record_file
    if os.path.isfile(date_range_record_file):
        with open(date_range_record_file, 'rb') as f:
            dates = pickle.load(f)
            if table_name in dates:
                return dates[table_name]
            else:
                return [None, None]
                return None
    else:
        # return [None, None]
        return None         

#%%
from datetime import date
from dateutil.rrule import rrule, DAILY, MONTHLY

def date_range(start_date, end_date):
    return [dt.date() for dt in rrule(DAILY, dtstart=start_date, until=end_date)]

def month_range(start_date, end_date):
    return [dt.date() for dt in rrule(MONTHLY, dtstart=start_date, until=end_date)]

def season_range(start_date, end_date):

    if isinstance(start_date, datetime.datetime):
        start_date = start_date.date()

    if isinstance(end_date, datetime.datetime):
        end_date = end_date.date()

    ret = []
    for year in range(start_date.year-1, end_date.year+1):
        ret += [  datetime.date(year, 5, 15),
                datetime.date(year, 8, 14),
                datetime.date(year, 11, 14),
                datetime.date(year+1, 3, 31)]
    ret = [r for r in ret if start_date < r < end_date]

    return ret