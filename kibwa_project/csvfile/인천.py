import pandas as pd
import math
import random
import re

csv_files = [
    '/work/neo/python/kibwa_project/csvfile/인천_2022.csv',
    '/work/neo/python/kibwa_project/csvfile/인천_2023.csv',
    '/work/neo/python/kibwa_project/csvfile/인천_2024.csv'
]

merged_df = pd.DataFrame()
for file in csv_files:
    match = re.search(r'20\d{2}', file)
    year = int(match.group()) if match else None
    df = pd.read_csv(file, encoding='cp949')
    df.columns = df.columns.str.strip()
    df = df[df['연료별'] == '전기'].copy()
    df['등록연도'] = year
    df['총합'] = df[['승용', '승합', '화물', '특수']].sum(axis=1)
    merged_df = pd.concat([merged_df, df], ignore_index=True)

df_grouped = merged_df.groupby(['시군구별', '등록연도'])['총합'].sum().reset_index()
df_pivot = df_grouped.pivot(index='시군구별', columns='등록연도', values='총합').sort_index(axis=1)

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
    max_val = row[2024] * 1.3 if 2024 in row and not pd.isna(row[2024]) else a * 1.3

    forecast = {}
    for i, year in enumerate(target_years):
        if year == 2022:
            forecast[year] = a
        else:
            forecast[year] = bounded_log_growth_from_base(i, a, max_val)

    predicted_rows.append({
        'sido': '인천광역시',
        'sigungu': region.strip(),
        **{str(year): round(forecast[year], 2) for year in target_years}
    })

df_result = pd.DataFrame(predicted_rows)
output_path = '/work/neo/python/kibwa_project/csvfile/incheon_2040.csv'
df_result.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"생성 완료: {output_path}")
