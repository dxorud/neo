import pandas as pd
import matplotlib.pyplot as plt

file_path = "한국교통안전공단_전국_전기차_차종별_용도별_차량_등록대수.csv" 
df = pd.read_csv(file_path, encoding='cp949')

regions = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종',
        '경기', '충북', '충남', '전남', '전북', '경북', '경남', '제주', '강원']

filtered_df = df[df['시도명'].isin(regions)]

region_counts = filtered_df.groupby('시도명')['등록대수'].sum().reindex(regions)

plt.figure(figsize=(12, 6))
bars = plt.bar(region_counts.index, region_counts.values, color='skyblue')
plt.title('광역시도별 전기차 등록 대수')
plt.xlabel('지역')
plt.ylabel('전기차 등록 대수')
plt.xticks(rotation=45)
plt.tight_layout()

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 200, f'{int(yval):,}', ha='center', va='bottom', fontsize=8)

filename = 'car1.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + ' saved')
plt.show()
