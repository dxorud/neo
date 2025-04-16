import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# 전기차 등록대수 데이터 로드
df = pd.read_csv('한국교통안전공단_전국_전기차_차종별_용도별_차량_등록대수.csv', encoding='cp949')
plt.rcParams['font.family'] = 'NanumBarunGothic'

# 시도명 추출 및 전체 차종 합계
df['시도명'] = df['시군구별'].str.split().str[0]
df['차종합계'] = df[['승용', '승합', '화물', '특수']].sum(axis=1)
grouped = df.groupby(['시도명', '용도별'])['차종합계'].sum().reset_index()
total_by_city = grouped.groupby('시도명')['차종합계'].sum()

# 1. 지도 이미지 불러오기
img = mpimg.imread('map.png')

# 2. 시도별 이미지 상의 위치 좌표 (지도에 맞게 직접 조정 필요!)
city_pixel_coords = {
    '서울': (510, 150),
    '부산': (780, 920),
    '대구': (680, 790),
    '인천': (460, 160),
    '광주': (430, 930),
    '대전': (540, 520),
    '울산': (750, 890),
    '세종': (540, 500),
    '경기': (500, 250),
    '강원': (650, 200),
    '충북': (580, 450),
    '충남': (490, 500),
    '전북': (500, 700),
    '전남': (490, 880),
    '경북': (670, 600),
    '경남': (690, 850),
    '제주': (400, 1150)
}

# 3. 그래프 시각화
fig, ax = plt.subplots(figsize=(10, 12))
ax.imshow(img)

for city, count in total_by_city.items():
    if city in city_pixel_coords:
        x, y = city_pixel_coords[city]
        size = count / 10  # 점 크기 비례
        ax.scatter(x, y, s=size, color='green', edgecolors='black', alpha=0.7)
        ax.text(x, y - 20, f"{city}\n{count:,}대", ha='center', fontsize=9)

plt.title('시도별 전기차 등록대수 (지도 이미지 기반)', fontsize=15)
plt.axis('off')
plt.tight_layout()
plt.savefig('전기차_지도_이미지기반_시각화.png', dpi=400)
plt.show()
