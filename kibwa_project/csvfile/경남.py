import pandas as pd
import math
import random

file_path = '/work/neo/python/kibwa_project/csvfile/경상남도_전기자동차 보급현황_20221231.csv'
df = pd.read_csv(file_path, encoding='cp949', on_bad_lines='skip')

df['구분'] = df['구분'].astype(int)
df = df.sort_values('구분').reset_index(drop=True)
df.set_index('구분', inplace=True)

df = df.reindex(range(2011, 2025))
df = df.interpolate(method='linear')

target_years = list(range(2022, 2041))

def bounded_log_growth_from_base(x, a, max_val, b=0.15, noise_level=0.03):
    base = a + (max_val - a) * math.log(b * x + 1) / math.log(b * (len(target_years) - 1) + 1)
    noise = random.uniform(-noise_level, noise_level) * base
    return base + noise

predicted_rows = []

for region in df.columns:
    if df.loc[2022, region] == 0 or pd.isna(df.loc[2022, region]):
        continue

    a = df.loc[2022, region]
    max_val = df.loc[2024, region] * 1.3 if not pd.isna(df.loc[2024, region]) else a * 1.3

    forecast = {}
    for i, year in enumerate(target_years):
        if year == 2022:
            forecast[year] = a
        else:
            forecast[year] = bounded_log_growth_from_base(i, a, max_val)

    predicted_rows.append({
        'sido': '경상남도',
        'sigungu': region.strip(),
        **{str(year): round(forecast[year], 2) for year in target_years}
    })

df_result = pd.DataFrame(predicted_rows)
output_path = '/work/neo/python/kibwa_project/csvfile/gyeongnam_2040.csv'
df_result.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"저장 완료: {output_path}")
