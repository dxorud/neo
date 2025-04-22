import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
plt.figure(figsize=(14, 10))

# 색상 설정: 각 년도를 다른 색으로 설정
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']

# 년월 이름을 변경 (원하는 이름으로 매핑)
year_month_map = {
    '2020-12': '2020년 12월',
    '2021-12': '2021년 12월',
    '2022-12': '2022년 12월',
    '2023-12': '2023년 12월',
    '2024-07': '2024년 7월'
}

# 누적 막대그래프 생성
bottom_values = np.zeros(len(region_data.index))  # 누적 값 초기화

for idx, date in enumerate(target_dates):
    bars = plt.barh(region_data.index, region_data[date], height=0.6, 
                    left=bottom_values, color=colors[idx], label=year_month_map[date])
    
    # 각 막대에 값 표시
    for bar in bars:
        width = bar.get_width()
        y_position = bar.get_y() + bar.get_height() / 2
        plt.text(width + 10, y_position, f'{width:.0f}', va='center', ha='left', fontsize=10)
    
    bottom_values += region_data[date]  # 누적 값 업데이트

    # 서울 지역에 대해 2020년, 2021년, 2022년, 2023년, 2024년 값 모두 그래프 안에 표시
    if date in target_dates:  # 모든 년도에 대해
        # 서울 지역의 위치와 해당 값 찾기
        seoul_value = region_data.loc['서울', date]
        seoul_y_pos = region_data.index.get_loc('서울')  # 서울의 y축 위치
        
        # 서울 지역의 각 년도 값 그래프 안에 표시
        plt.text(seoul_value / 2, seoul_y_pos, f'{seoul_value:.0f}', 
                va='center', ha='center', fontsize=12, color='white', fontweight='bold')

plt.title('연도별 전기차 등록 대수 (지역별)', fontsize=15)
plt.xlabel('전기차 등록 대수', fontsize=12)
plt.ylabel('지역', fontsize=12)
plt.legend(title='년월')
plt.grid(axis='x', linestyle='--', alpha=0.4)
plt.tight_layout()

filename = 'car_stacked_bar_with_seoul_values.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + ' saved')
plt.show()
