from pandas import *
import pandas as pd
import numpy as np
import json
df = pd.DataFrame(json.loads(input()))
## 1. Sort Dataframe
# print(df)
# result = df.sort_values(by=['Fee', 'Discount'], ascending=[False, True])
# print(result)
# res_dict = result.to_dict(orient='list')
# print(json.dumps(res_dict))

## 2. Repetitive barcode
# res = pd.DataFrame(df.loc[df.duplicated(keep=False, subset='barcode'),:])
# res_dict = dict(res.groupby('barcode')['sample_name'].apply(list))
# print(json.dumps(res_dict))

## 3. Average Score
# res = pd.DataFrame(df.groupby('name', as_index=False).mean())
# res['score'] = round(res['score'], 2)
# print(json.dumps(res.to_dict('list')))

## 4. First Names Only
# import re
# name_list = df['name'].tolist()
# new_list = []
# for i in name_list:
#     new_list.append(re.sub(r'\s.+', '', i))
#
# df.loc[:, 'name'] = new_list
# print(json.dumps(df.to_dict('list')))

## 5. Good Grades and Favorite Colors
# def grades_color(df: pd.DataFrame):
#     judge = (df['grade'] > 90) & ((df['favorite_color'] == 'red') | (df['favorite_color'] == 'green'))
#     res = df.loc[judge, :]
#     return res
#
#
# res = grades_color(df)
# print(json.dumps(res.to_dict('list')))

