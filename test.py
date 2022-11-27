#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 14:35:52 2022

@author: jacob
"""

import pandas as pd
import datetime
df = pd.read_pickle(r'/Users/jacob/Library/CloudStorage/OneDrive-個人/桌面/Quan/history/tables/price.pkl')

df = df.apply(lambda x:pd.to_numeric(x ,errors = 'coerce'))
df = df.reset_index()



!pip freeze > requirements.txt

# df.index[-1][1]+ datetime.timedelta(days=1)


