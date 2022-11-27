#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 20:14:08 2022

@author: jacob
"""
from Crawler.Process import *

date_range_record_file = os.path.join('history', 'date_range.pickle')


def update_table(table_name, crawl_function, dates):

    if dates:
        if len(dates) == 0:
            print("該時間段沒有可以爬取之資料")
            # return
        print(f'start crawl {table_name} from ', dates[0] , 'to', dates[-1])
        # print({dates[0]} to {dates[-1]})
    else:
        print('起始、結束日期有點怪怪的，請重新選擇一下喔，下載財報時，可以用以下的選法')
        print('第一季：該年 5/1~5/31')
        print('第二季：該年 8/1~8/31')
        print('第三季：該年 11/1~11/30')
        print('第四季：隔年 3/1~4/31')
        # return


    df = pd.DataFrame()
    dfs = {}

    progress = tqdm_notebook(dates, )
    
    for d in progress:

        print(f'crawling {d}')
        # print('crawling', d, end="")
        progress.set_description(f'crawl {table_name} {d}')
        # progress.set_description('crawl' + table_name + str(d))

        data = crawl_function(d)

        if data is None or len(data) == 0:
            print('  ❌')

        # update multiple dataframes
        elif isinstance(data, dict):
            if len(dfs) == 0:
                dfs = {i:pd.DataFrame() for i in data.keys()}

            for i, d in data.items():
                # dfs[i] = dfs[i].append(d)
                dfs[i] = pd.concat([dfs[i],d])

        # update single dataframe
        else:
            # df = df.append(data)
            df = pd.concat([df,data])
            print('  ✅')

        time.sleep(10)


    
    if df is not None and len(df) != 0:
        to_SQL(df, table_name)

    if len(dfs) != 0:
        for i, d in dfs.items():
            if len(d) != 0:
                to_SQL(df, table_name)
                
                
def to_SQL(df, table_name):

    # if not os.path.isdir('history'):
    #     os.mkdir('history')

    # if not os.path.isdir(os.path.join('history', 'tables')):
    #     os.mkdir(os.path.join('history', 'tables'))
    
    localhost='3306'
    database='Quant'
    user='root'
    password='Aaa710258' 
    engine = sqlalchemy.create_engine(f"mysql+pymysql://{user}:{password}@localhost:{localhost}/{database}")
    
    cnx = engine.connect()

    df = df.apply(lambda x:pd.to_numeric(x ,errors = 'coerce'))
    df = df.reset_index()
       
    df.to_sql(table_name
                  , cnx
                  , if_exists='append'
                  , index=False)
    
    global date_range_record_file
    #儲存下次爬取的時間點
    if not os.path.isfile(date_range_record_file):
        pickle.dump({}, open(date_range_record_file, 'wb'))
    
    TimeStamp = pickle.load(open(date_range_record_file, 'rb'))
    TimeStamp[table_name] = df.sort_values('date',ascending = False)['date'].iloc[0]
    # TimeStamp[table_name] = (df.index.levels[1][0], df.index.levels[1][-1] + datetime.timedelta(days=1))
    pickle.dump(TimeStamp, open(date_range_record_file, 'wb'))

