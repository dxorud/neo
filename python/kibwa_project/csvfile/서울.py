import pandas as pd
from pymongo import MongoClient
import re

file_path = '/work/neo/python/kibwa_project/csvfile/서울_(2017-2022).csv'

df = pd.read_csv(file_path, encoding='cp949')
df.columns = df.columns.str.strip().str.replace(' ', '').str.replace('\n', '')
print("컬럼명:", df.columns.tolist())

df = df[df['연료별'] == '전기'].copy()

df['연도'] = df['연월별'].str.extract(r'(\d{4})').astype(int)

df['총합'] = df[['승용', '승합', '화물', '특수']].sum(axis=1)

df_grouped = df.groupby(['시군구별', '연도'])['총합'].sum().reset_index()

df_pivot = df_grouped.pivot(index='시군구별', columns='연도', values='총합')
df_pivot = df_pivot.sort_index(axis=1)

predicted_rows = []
for region, row in df_pivot.iterrows():
    available_years = row.dropna().index.tolist()
    if len(available_years) < 2:
        continue

    recent_years = sorted(available_years)[-3:]
    recent_values = row[recent_years].values
    diffs = [recent_values[i] - recent_values[i - 1] for i in range(1, len(recent_values))]
    avg_increase = sum(diffs) / len(diffs)

    val_2022 = row.get(2022, recent_values[-1])
    val_2023 = val_2022 + avg_increase
    val_2024 = val_2023 + avg_increase

    predicted_rows.append({
        'region': region,
        '2022': round(val_2022, 2),
        '2023': round(val_2023, 2),
        '2024': round(val_2024, 2)
    })

df_result = pd.DataFrame(predicted_rows)

client = MongoClient('mongodb://192.168.1.44:27017/')
db = client['electric_car']
collection = db['seoul_ev_forecast']

sido_name = "서울특별시"  

for _, row in df_result.iterrows():
    full_region = f"{sido_name} {row['region']}".strip()
    doc = {
        'region': full_region,
        'yearly_data': {
            '2022': row['2022'],
            '2023': row['2023'],
            '2024': row['2024'],
        }
    }
    collection.update_one(
        {'region': full_region},
        {'$set': doc},
        upsert=True
    )

print("'서울특별시 시군구' 형식으로 MongoDB(seoul_ev_forecast)에 저장 완료!")
