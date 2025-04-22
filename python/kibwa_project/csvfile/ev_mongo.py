import pandas as pd
import os
from pymongo import MongoClient

client = MongoClient('mongodb://192.168.1.44:27017/')
db = client['electric_car']

csv_dir = '/work/neo/python/kibwa_project/csvfile'
csv_files = [
    'seoul_2040.csv',
    'gyeonggi_2040.csv',
    'incheon_2040.csv',
    'chungbuk_2040.csv',
    'jeonnam_2040.csv',
    'gyeongnam_2040.csv'
]

collection_map = {
    'seoul': 'seoul_ev_forecast',
    'gyeonggi': 'gyeonggi_ev_forecast',
    'incheon': 'incheon_ev_forecast',
    'chungbuk': 'chungbuk_ev_forecast',
    'jeonnam': 'jeonnam_ev_forecast',
    'gyeongnam': 'gyeongnam_ev_forecast'
}

for file_name in csv_files:
    key = file_name.split('_')[0].lower()
    collection_name = collection_map.get(key, '')
    full_path = os.path.join(csv_dir, file_name)

    df = pd.read_csv(full_path, encoding='utf-8-sig')
    collection = db[collection_name]

    for _, row in df.iterrows():
        sido = row['sido']
        sigungu = row['sigungu']

        doc = {
            'sido': sido,
            'sigungu': sigungu
        }

        for col in df.columns:
            if col not in ['sido', 'sigungu']:
                doc[col] = row[col]

        collection.update_one(
            {'sido': sido, 'sigungu': sigungu},
            {'$set': doc},
            upsert=True
        )

    print(f"[{file_name}] → '{collection_name}' 저장 완료")
