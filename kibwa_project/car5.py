import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams['font.family'] = 'NanumBarunGothic'

# CSV 불러오기
file_path = '202012202412전기차등록현황.csv'
df = pd.read_csv(file_path, encoding='utf-8-sig')

# 첫 번째 열 이름 변경
df.rename(columns={df.columns[0]: '년월'}, inplace=True)

# '년월'을 문자열로 변환
df['년월'] = df['년월'].astype(str)

# 사용할 연도 리스트 (실제 존재하는 12월)
target_months = ['2020-12', '2021-12', '2022-12', '2023-12', '2024-07']

# 해당 연도만 필터링
df_filtered = df[df['년월'].isin(target_months)]

# '년월'을 인덱스로 설정
df_filtered.set_index('년월', inplace=True)

# 행과 열을 전치해서 지역이 행, 연도가 열이 되게 함
df_transposed = df_filtered.T

# 그래프 설정
plt.figure(figsize=(14, 8))

# 컬러 리스트 (필요에 따라 더 추가 가능)
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '#FF6347', '#8A2BE2', '#3CB371',
        '#FFD700', '#00CED1', '#DC143C', '#9932CC', '#FF4500', '#556B2F', '#1E90FF']

# 지역별 그래프 그리기
for i, region in enumerate(df_transposed.index):
    plt.plot(df_transposed.columns, df_transposed.loc[region],
            label=region, color=colors[i % len(colors)], marker='o')

plt.title('지역별 전기차 등록 변화 (12월 기준)', fontsize=16)
plt.xlabel('연도', fontsize=14)
plt.ylabel('등록 대수', fontsize=14)
plt.legend(title='지역', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()

# 저장 및 출력
filename = 'car5.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + ' 저장 완료')

plt.show()
