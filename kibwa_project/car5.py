import pandas as pd
import matplotlib.pyplot as plt

file_path = '202012202412전기차등록현황.csv'

# CSV 파일 읽기
df = pd.read_csv(file_path, encoding='utf-8', header=0)
plt.rcParams['font.family'] = 'NanumBarunGothic'

# 열 이름, '년월' 컬럼 공백 제거
df.columns = df.columns.str.strip()
df['년월'] = df['년월'].astype(str).str.strip()

# 필터링할 년월 리스트
target_dates = ['2020-12', '2021-12', '2022-12', '2023-12', '2024-07']
filtered = df[df['년월'].isin(target_dates)]

# '합계' 컬럼 제거하고, 년월을 인덱스로 설정
filtered = filtered.drop(columns=['합계'])
filtered = filtered.set_index('년월')

# 행/열 전치해서 지역 기준으로 변환
region_data = filtered.T
region_data.index.name = '지역'

# 시각화
plt.figure(figsize=(14, 7))

for date in target_dates:
    plt.plot(region_data.index, region_data[date], marker='o', label=date)

plt.title('연도별 전기차 등록 대수 (지역별)', fontsize=15)
plt.xlabel('지역', fontsize=12)
plt.ylabel('전기차 등록 대수', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='년월')
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout()

filename = 'car5.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + ' saved')
plt.show()
