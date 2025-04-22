import pandas as pd
import math
import random

file_path = '/work/neo/python/kibwa_project/csvfile/충청북도_전기자동차_보급_현황.csv'

df = pd.read_csv(file_path, encoding='utf-8')
df.columns = df.columns.str.strip().str.replace(' ', '').str.replace('\n', '')

df = df[~df['연도'].astype(str).str.contains('이전')]
df['연도'] = df['연도'].astype(int)
df = df.drop(columns=['도'], errors='ignore')

df_melted = df.melt(id_vars='연도', var_name='region', value_name='count')
df_pivot = df_melted.pivot(index='region', columns='연도', values='count')
df_pivot = df_pivot.apply(pd.to_numeric, errors='coerce').fillna(0)

target_years = list(range(2022, 2041))

def bounded_log_growth(x, max_val=10000, b=0.15, noise_level=0.03):
    base = max_val * math.log(b * x + 1) / math.log(b * (len(target_years) - 1) + 1)
    noise = random.uniform(-noise_level, noise_level) * base
    return base + noise

predicted_rows = []

for region, row in df_pivot.iterrows():
    available_years = [year for year in row.dropna().index.tolist() if year >= 2016]
    if len(available_years) < 2:
        continue

    values = row[available_years].values
    last_val = values[-1]
    max_val = last_val * 1.3  

    forecast = {}
    for i, year in enumerate(target_years):
        if year in row:
            forecast[year] = row[year]
        else:
            forecast[year] = bounded_log_growth(i, max_val=max_val)

    predicted_rows.append({
        'sido': '충청북도',
        'sigungu': region.strip(),
        **{str(year): round(forecast[year], 2) for year in target_years}
    })

df_result = pd.DataFrame(predicted_rows)
output_path = '/work/neo/python/kibwa_project/csvfile/chungbuk_2040.csv'
df_result.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"저장 완료: {output_path}")
