import pandas as pd
from pymongo import MongoClient

file_path = '/work/neo/python/kibwa_project/csvfile/전라남도_전기자동차 등록현황.csv'

df = pd.read_csv(file_path, encoding='cp949')
df.columns = df.columns.str.strip().str.replace(' ', '').str.replace('\n', '')

df_ev = df[['시군명', '전기승용22년', '전기승용23년', '전기승용24년6월']].copy()
df_ev.columns = ['region', '2022', '2023', '2024']

df_ev = df_ev.dropna()
df_ev[['2022', '2023', '2024']] = df_ev[['2022', '2023', '2024']].astype(int)

df_ev['increase_23'] = df_ev['2023'] - df_ev['2022']
df_ev['increase_24'] = df_ev['2024'] - df_ev['2023']
df_ev['avg_increase'] = ((df_ev['increase_23'] + df_ev['increase_24']) / 2).round()

df_ev['2023_predicted'] = (df_ev['2022'] + df_ev['avg_increase']).round()
df_ev['2024_predicted'] = (df_ev['2023_predicted'] + df_ev['avg_increase']).round()

df_final = df_ev[['region', '2022', '2023_predicted', '2024_predicted']].copy()
df_final.columns = ['region', '2022', '2023', '2024']

client = MongoClient('mongodb://192.168.1.44:27017/')
db = client['electric_car']
collection = db['jeonnam_ev_forecast']

sido_name = "전라남도"

for _, row in df_final.iterrows():
    full_region = f"{sido_name} {row['region']}".strip()

    doc = {
        'region': full_region,
        'yearly_data': {
            '2022': int(row['2022']),
            '2023': int(row['2023']),
            '2024': int(row['2024'])
        }
    }
    collection.update_one(
        {'region': full_region},
        {'$set': doc},
        upsert=True
    )

print("전라남도 전기차 예측 데이터를 시도+시군구 형식으로 MongoDB에 저장 완료!")
