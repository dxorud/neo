import pandas as pd
from pymongo import MongoClient
import re

csv_files = [
    '/work/neo/python/kibwa_project/csvfile/인천_2022.csv',
    '/work/neo/python/kibwa_project/csvfile/인천_2023.csv',
    '/work/neo/python/kibwa_project/csvfile/인천_2024.csv'
]

merged_df = pd.DataFrame()

for file in csv_files:
    match = re.search(r'20\d{2}', file)
    if match:
        year = int(match.group())
    else:
        raise ValueError(f"파일명에서 연도를 찾을 수 없습니다: {file}")

    df = pd.read_csv(file, encoding='cp949')
    df.columns = df.columns.str.strip()
    print(f"[{file}] → 컬럼명:", df.columns.tolist())

    df = df[df['연료별'] == '전기'].copy()
    df['등록연도'] = year
    df['총합'] = df[['승용', '승합', '화물', '특수']].sum(axis=1)

    merged_df = pd.concat([merged_df, df], ignore_index=True)

df_grouped = merged_df.groupby(['시군구별', '등록연도'])['총합'].sum().reset_index()
df_pivot = df_grouped.pivot(index='시군구별', columns='등록연도', values='총합').fillna(0)

client = MongoClient('mongodb://192.168.1.44:27017/')
db = client['electric_car']
collection = db['incheon_ev_actual']

sido = "인천광역시"  

for region, row in df_pivot.iterrows():
    full_region = f"{sido} {region}".strip() 
    doc = {
        'region': full_region,
        'yearly_data': {
            '2022': int(row.get(2022, 0)),
            '2023': int(row.get(2023, 0)),
            '2024': int(row.get(2024, 0)),
        }
    }
    collection.update_one(
        {'region': full_region},
        {'$set': doc},
        upsert=True
    )

print("인천 전기차 2022~2024년 데이터를 MongoDB에 성공적으로 저장했습니다! (시도+시군구 형식)")
