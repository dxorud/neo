import pandas as pd
from pymongo import MongoClient

file_path = '/work/neo/python/kibwa_project/csvfile/경상남도_전기자동차 보급현황_20221231.csv'
df = pd.read_csv(file_path, encoding='cp949', on_bad_lines='skip')

df['구분'] = df['구분'].astype(int)
df = df.sort_values('구분').reset_index(drop=True)

df.set_index('구분', inplace=True)

df = df.reindex(list(range(2011, 2025))) 
df = df.interpolate(method='linear') 

subset = df.loc[2022:2024]

client = MongoClient("mongodb://192.168.1.44:27017/")
db = client["ev_database"]
collection = db["gyeongnam_forecast"]

for year, row in subset.iterrows():
    data = {
        "year": int(year),
        "data": row.to_dict()
    }
    collection.insert_one(data)

print("MongoDB에 2022~2024년 예측 데이터 저장 완료!")
