import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 경로
file_path = '한국교통안전공단_전국_전기차_차종별_용도별_차량_등록대수.csv'

# CSV 파일 읽기
df = pd.read_csv(file_path, encoding='cp949')
plt.rcParams['font.family'] = 'NanumBarunGothic'

# 시도명 추출: '서울 중구' -> '서울'
df['시도명'] = df['시군구별'].str.split().str[0]

# 승용, 승합, 화물, 특수 합산하여 '차종합계' 열 생성
df['차종합계'] = df[['승용', '승합', '화물', '특수']].sum(axis=1)

# 시도명 + 용도별 그룹으로 묶어서 차종합계 합산
grouped = df.groupby(['시도명', '용도별'])['차종합계'].sum().reset_index()

# 시도별 전체(사업용+비사업용) 차량 수 계산
total_by_city = grouped.groupby('시도명')['차종합계'].sum().sort_values()

# 가로 막대 그래프 출력
plt.figure(figsize=(12, 8))
plt.barh(total_by_city.index, total_by_city.values, color='skyblue')
plt.xlabel('전기차 등록 대수')
plt.ylabel('시도명')
plt.title('시도별 전기차 등록 대수 (사업용 + 비사업용, 차종 전체 합산)')
plt.tight_layout()
plt.grid(axis='x', linestyle='--', alpha=0.5)

filename = 'car1.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + ' saved')
plt.show()
