#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 14:35:52 2022

@author: jacob
"""
from Crawler.Process import *
from Crawler.SaveData import *
from Crawler.ptt import *


table_name='Gossiping'
end_page = new_page(table_name) #取得最新頁面
start_page=table_date_range(table_name)
if start_page == None:
    start_page = int(end_page/3)
AllPage = [_ for _ in range(start_page, end_page, 1)]



progress = tqdm_notebook(AllPage, )

date_range_record_file = os.path.join('history', 'date_range.pickle')


for page in progress:

    df = crawler(table_name,page)
    if df is None or len(df) == 0:
        print(f'{page}  ❌')
    else:
        print(f'{page}  ✅')
        Save = to_CSV(table_name,platform='PTT')
        Save.add_to_csv(df, TimeColumn = '日期')
        # global date_range_record_file
        #儲存下次爬取的時間點
        if not os.path.isfile(date_range_record_file):
            pickle.dump({}, open(date_range_record_file, 'wb'))
        
        
        
        index = '頁數'
        TimeStamp = pickle.load(open(date_range_record_file, 'rb'))
        TimeStamp[table_name] = df.sort_values(index,ascending = False)[index].iloc[0]
        
        pickle.dump(TimeStamp, open(date_range_record_file, 'wb'))
        

