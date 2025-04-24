import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. 파일 읽기 및 기본 설정
file_path = 'ev.csv'
df = pd.read_csv(file_path, encoding='utf-8', header=0)
plt.rcParams['font.family'] = 'NanumBarunGothic'

# 2. 컬럼 정리
df.columns = df.columns.str.strip()
df['년월'] = df['년월'].astype(str).str.strip()

# 3. 대상 년월 필터링
target_dates = ['2020-12', '2021-12', '2022-12', '2023-12', '2024-07']
filtered = (
    df[df['년월'].isin(target_dates)]
      .drop(columns=['합계'])
      .set_index('년월')
)

# 4. 지역 기준으로 전치
region_data = filtered.T
region_data.index.name = '지역'

# 5. 지역별 총합 계산 후 내림차순 정렬
region_data['Total'] = region_data.sum(axis=1)
region_data = region_data.sort_values(by='Total', ascending=False)
region_data = region_data.drop(columns=['Total'])

# 6. 시각화 준비
plt.figure(figsize=(14, 10))

# 따뜻한 톤 팔레트
colors = [
    '#FF8A65',  # 따뜻한 오렌지
    '#FFB74D',  # 연한 오렌지
    '#FFD54F',  # 햇살 옐로우
    '#FFF176',  # 파스텔 옐로우
    '#F06292',  # 핑크 포인트
]

# 년월 라벨 매핑
year_month_map = {
    '2020-12': '2020년 12월',
    '2021-12': '2021년 12월',
    '2022-12': '2022년 12월',
    '2023-12': '2023년 12월',
    '2024-07': '2024년 7월'
}

bottom_values = np.zeros(len(region_data))

# 7. 누적 가로 막대그래프 그리기 (레이블 없음)
for idx, date in enumerate(target_dates):
    plt.barh(
        region_data.index,
        region_data[date],
        height=0.6,
        left=bottom_values,
        color=colors[idx],
        label=year_month_map[date]
    )
    bottom_values += region_data[date]

# 8. Y축 뒤집기 → 가장 큰 값이 맨 위
plt.gca().invert_yaxis()

# 9. 레이블·타이틀·그리드
plt.title('연도별 전기차 등록 대수 (지역별)', fontsize=15)
plt.xlabel('전기차 등록 대수', fontsize=12)
plt.ylabel('지역', fontsize=12)
plt.legend(title='년월')
plt.grid(axis='x', linestyle='--', alpha=0.4)
plt.tight_layout()

# 10. 파일 저장 및 출력
filename = 'car_warmtone.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(f'{filename} saved')
plt.show()
