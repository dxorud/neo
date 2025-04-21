import pandas as pd
from pymongo import MongoClient

file_path = '/work/neo/python/kibwa_project/csvfile/충청북도_전기자동차_보급_현황.csv'

df = pd.read_csv(file_path, encoding='utf-8')
df.columns = df.columns.str.strip().str.replace(' ', '').str.replace('\n', '')

df = df[~df['연도'].astype(str).str.contains('이전')]
df['연도'] = df['연도'].astype(int)
df = df.drop(columns=['도'], errors='ignore')

df_melted = df.melt(id_vars='연도', var_name='region', value_name='count')
df_pivot = df_melted.pivot(index='region', columns='연도', values='count')
df_pivot = df_pivot.apply(pd.to_numeric, errors='coerce').fillna(0)

df_pivot[2023] = df_pivot[2022] + (df_pivot[2022] - df_pivot[2021])
df_pivot[2024] = df_pivot[2023] + (df_pivot[2023] - df_pivot[2022])

df_final = df_pivot[[2022, 2023, 2024]].reset_index()

client = MongoClient('mongodb://192.168.1.44:27017/')
db = client['electric_car']
collection = db['chungbuk_ev_forecast']

sido_name = "충청북도" 

for _, row in df_final.iterrows():
    full_region = f"{sido_name} {row['region']}".strip()
    doc = {
        'region': full_region,
        'yearly_data': {
            '2022': int(row[2022]),
            '2023': int(row[2023]),
            '2024': int(row[2024])
        }
    }
    collection.update_one(
        {'region': full_region},
        {'$set': doc},
        upsert=True
    )

print("충청북도 전기차 2022~2024 예측 데이터를 시도+시군구 형식으로 MongoDB에 저장 완료했습니다.")
