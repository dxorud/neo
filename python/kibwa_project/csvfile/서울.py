import pandas as pd
import numpy as np
import math
import random
import re

file_path = '/work/neo/python/kibwa_project/csvfile/서울_(2017-2022).csv'
df = pd.read_csv(file_path, encoding='cp949')
df.columns = df.columns.str.strip().str.replace(' ', '').str.replace('\n', '')

df = df[df['연료별'] == '전기'].copy()
df['연도'] = df['연월별'].str.extract(r'(\d{4})').astype(int)
df['총합'] = df[['승용', '승합', '화물', '특수']].sum(axis=1)

df_grouped = df.groupby(['시군구별', '연도'])['총합'].sum().reset_index()
df_pivot = df_grouped.pivot(index='시군구별', columns='연도', values='총합').sort_index(axis=1)

target_years = list(range(2022, 2041))

def bounded_log_growth_from_base(x, a, max_val, b=0.15, noise_level=0.03):
    base = a + (max_val - a) * math.log(b * x + 1) / math.log(b * (len(target_years) - 1) + 1)
    noise = random.uniform(-noise_level, noise_level) * base
    return base + noise

predicted_rows = []

for region, row in df_pivot.iterrows():
    if 2022 not in row or pd.isna(row[2022]):
        continue

    a = row[2022]
    recent_max = row[max(row.dropna().index)]
    max_val = recent_max * 1.3  

    forecast = {}
    for i, year in enumerate(target_years):
        if year == 2022:
            forecast[year] = a
        else:
            forecast[year] = bounded_log_growth_from_base(i, a, max_val)

    predicted_rows.append({
        'sido': '서울특별시',
        'sigungu': region.strip(),
        **{str(year): round(forecast[year], 2) for year in target_years}
    })

df_result = pd.DataFrame(predicted_rows)
output_path = '/work/neo/python/kibwa_project/csvfile/seoul_2040.csv'
df_result.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"생성 완료: {output_path}")
