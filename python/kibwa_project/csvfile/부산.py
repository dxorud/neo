import pandas as pd
from pymongo import MongoClient

# 연도별 파일 경로
csv_files = {
    "/work/neo/python/kibwa_project/csvfile/부산등록현황_2021.csv": 2021,
    "/work/neo/python/kibwa_project/csvfile/부산등록현황_2022.csv": 2022,
    "/work/neo/python/kibwa_project/csvfile/부산등록현황_2023.csv": 2023
}

all_data = []

for file, year in csv_files.items():
    # 1. 파일 읽기 (첫 줄부터 헤더)
    df = pd.read_csv(file, encoding='utf-8')
    df.columns = df.columns.astype(str).str.strip().str.replace(' ', '').str.replace('\n', '')

    # 2. 지역명 컬럼 통일
    df = df.rename(columns={df.columns[0]: 'region'})

    # 3. 전기 관련 열만 추출
    ev_cols = [col for col in df.columns if col.startswith('전기')]

    # 4. 숫자형 변환 (쉼표 제거 후 float)
    df[ev_cols] = df[ev_cols].replace(',', '', regex=True).apply(pd.to_numeric, errors='coerce').fillna(0)

    # 5. 전기차 등록 대수 합산
    df['등록대수'] = df[ev_cols].sum(axis=1)
    df['연도'] = year

    # 6. 필요한 컬럼만 저장
    all_data.append(df[['region', '연도', '등록대수']])

# 7. 연도별 병합 및 피벗
merged_df = pd.concat(all_data, ignore_index=True)
pivot_df = merged_df.pivot(index='region', columns='연도', values='등록대수').fillna(0)

# 8. 선형 예측: 2024 = 2023 + (2023 - 2022)
pivot_df[2024] = pivot_df[2023] + (pivot_df[2023] - pivot_df[2022])

# 9. 최종 정리
df_final = pivot_df[[2022, 2023, 2024]].reset_index()

# 10. MongoDB 저장
client = MongoClient("mongodb://192.168.1.44:27017/")
db = client["electric_car"]
collection = db["busan_ev_forecast"]

for _, row in df_final.iterrows():
    doc = {
        "region": row["region"],
        "yearly_data": {
            "2022": int(row[2022]),
            "2023": int(row[2023]),
            "2024": int(row[2024])
        }
    }
    collection.update_one({"region": row["region"]}, {"$set": doc}, upsert=True)

print("✅ 부산 전기차 등록대수 (2022~2024) MongoDB 저장 완료!")
