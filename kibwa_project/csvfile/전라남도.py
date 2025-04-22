import pandas as pd
import math
import random

file_path = '/work/neo/python/kibwa_project/csvfile/전라남도_전기자동차 등록현황.csv'
df = pd.read_csv(file_path, encoding='cp949')
df.columns = df.columns.str.strip().str.replace(' ', '').str.replace('\n', '')

df_ev = df[['시군명', '전기승용22년', '전기승용23년', '전기승용24년6월']].copy()
df_ev.columns = ['region', '2022', '2023', '2024']
df_ev = df_ev.dropna()
df_ev[['2022', '2023', '2024']] = df_ev[['2022', '2023', '2024']].astype(int)

target_years = list(range(2022, 2041))

def bounded_log_growth_from_base(x, a, max_val, b=0.15, noise_level=0.03):
    base = a + (max_val - a) * math.log(b * x + 1) / math.log(b * 18 + 1)
    noise = random.uniform(-noise_level, noise_level) * base
    return base + noise

predicted_rows = []

for _, row in df_ev.iterrows():
    region = row['region']
    a = row['2022']
    max_val = row['2024'] * 1.3

    forecast = {}
    for i, year in enumerate(target_years):
        if year == 2022:
            forecast[year] = a
        else:
            forecast[year] = bounded_log_growth_from_base(i, a, max_val)

    predicted_rows.append({
        'sido': '전라남도',
        'sigungu': region.strip(),
        **{str(year): round(forecast[year], 2) for year in target_years}
    })

df_result = pd.DataFrame(predicted_rows)

output_path = '/work/neo/python/kibwa_project/csvfile/jeonnam_2040.csv'
df_result.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"생성 완료: {output_path}")
