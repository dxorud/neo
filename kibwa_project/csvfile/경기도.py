import pandas as pd
import math
import random

file_path = '/work/neo/python/kibwa_project/csvfile/경기도.csv'
df = pd.read_csv(file_path, encoding='cp949')
df.columns = df.columns.str.strip()

df_ev = df[df['연료별'] == '전기'].copy()
df_ev['총합'] = df_ev[['승용차수', '승합차수', '특수차수', '화물차수']].sum(axis=1)
df_ev['등록연도'] = df_ev['등록연도'].astype(int)
df_ev = df_ev[df_ev['등록연도'] >= 2019]

df_grouped = df_ev.groupby(['시군구명', '등록연도'])['총합'].sum().reset_index()
df_pivot = df_grouped.pivot(index='시군구명', columns='등록연도', values='총합').sort_index(axis=1)

def bounded_log_growth_from_base(x, a, max_val, b=0.15, noise_level=0.03):
    base = a + (max_val - a) * math.log(b * x + 1) / math.log(b * 18 + 1)
    noise = random.uniform(-noise_level, noise_level) * base
    return base + noise

target_years = list(range(2022, 2041))
predicted_rows = []

for region, row in df_pivot.iterrows():
    if 2022 not in row or pd.isna(row[2022]):
        continue

    a = row[2022]
    max_val = a * 1.3 

    forecast = {}
    for i, year in enumerate(target_years):
        if year == 2022:
            forecast[year] = a
        else:
            forecast[year] = bounded_log_growth_from_base(i, a, max_val)

    predicted_rows.append({
        'sido': '경기도',
        'sigungu': region.strip(),
        **{str(year): round(forecast[year], 2) for year in target_years}
    })

df_predicted = pd.DataFrame(predicted_rows)
csv_output_path = '/work/neo/python/kibwa_project/csvfile/gyeonggi_2040.csv'
df_predicted.to_csv(csv_output_path, index=False, encoding='utf-8-sig')

print(f"저장 완료: {csv_output_path}")
