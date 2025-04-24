import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 경로
file_path = '한국교통안전공단_전국_전기차_차종별_용도별_차량_등록대수.csv'

# CSV 파일 읽기
df = pd.read_csv(file_path, encoding='cp949')
plt.rcParams['font.family'] = 'NanumBarunGothic'  # 한글 폰트 설정

# 시도명 추출
df['시도명'] = df['시군구별'].str.split().str[0]

# 차종합계 열 생성
df['차종합계'] = df[['승용', '승합', '화물', '특수']].sum(axis=1)

# 시도 + 용도별로 그룹화 후 합계 계산
grouped = df.groupby(['시도명', '용도별'])['차종합계'].sum().reset_index()
total_by_city = grouped.groupby('시도명')['차종합계'].sum()

# 상위 3개, 하위 3개 추출
top_3 = total_by_city.nlargest(3)
bottom_3 = total_by_city.nsmallest(3) * -1  # 음수로 변환해서 왼쪽으로

# 병합 및 순서 정렬
combined = pd.concat([bottom_3, top_3])
combined = combined.sort_values()

# 색상 리스트 생성
colors = ['blue'] * 3 + ['red'] * 3  # 하위 3개: 파란색, 상위 3개: 빨간색

# 그래프 그리기
plt.figure(figsize=(10, 6))
bars = plt.barh(combined.index, combined.values, color=colors)

# 기준선 (중앙 0선)
plt.axvline(0, color='black', linewidth=1)

# 값 레이블 추가
for bar in bars:
    width = bar.get_width()
    plt.text(width + (300 if width > 0 else -300),
            bar.get_y() + bar.get_height() / 2,
            f'{abs(int(width)):,}',
            va='center',
            ha='left' if width > 0 else 'right',
            fontsize=10)

# 축, 제목
plt.xlabel('전기차 등록 대수')
plt.title('상위 3개 vs 하위 3개 지역 전기차 등록 대수 (양방향 비교)')
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()

# 저장 및 출력
filename = 'car3.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + ' saved')
plt.show()
