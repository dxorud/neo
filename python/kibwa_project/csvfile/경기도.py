import pandas as pd
from pymongo import MongoClient

file_path = '/work/neo/python/kibwa_project/csvfile/경기도.csv'

df = pd.read_csv(file_path, encoding='cp949')
df.columns = df.columns.str.strip()

df_ev = df[df['연료별'] == '전기'].copy()
df_ev['총합'] = df_ev[['승용차수', '승합차수', '특수차수', '화물차수']].sum(axis=1)
df_ev['등록연도'] = df_ev['등록연도'].astype(int)

df_grouped = df_ev.groupby(['시군구명', '등록연도'])['총합'].sum().reset_index()
df_pivot = df_grouped.pivot(index='시군구명', columns='등록연도', values='총합').sort_index(axis=1)

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
        '2022': val_2022,
        '2023': val_2023,
        '2024': val_2024
    })

df_predicted = pd.DataFrame(predicted_rows)

client = MongoClient('mongodb://192.168.1.44:27017/')
db = client['electric_car']
collection = db['gyeonggi_ev_forecast']

sido = "경기도" 

for _, row in df_predicted.iterrows():
    full_region = f"{sido} {row['region']}".strip()
    doc = {
        'region': full_region,
        'yearly_data': {
            '2022': round(row['2022'], 2),
            '2023': round(row['2023'], 2),
            '2024': round(row['2024'], 2)
        }
    }
    collection.update_one(
        {'region': full_region},
        {'$set': doc},
        upsert=True
    )

print("경기도 전기차 예측 데이터를 '시도 + 시군구' 형태로 MongoDB에 성공적으로 저장했습니다!")
