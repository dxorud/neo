import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

# 폰트 설정
plt.rcParams['font.family'] = 'NanumBarunGothic'
mpl.rcParams['axes.unicode_minus'] = False

# CSV 파일 경로
file_path = '지역별_전기차_충전기_구축현황(누적).csv'
df = pd.read_csv(file_path, encoding='utf-8')
df.columns = df.columns.str.strip()

# 사용할 년월 리스트 (급속 충전소 데이터)
target_months = ['2020-12', '2021-12', '2022-12', '2023-12', '2024-12']
regions = ['서울', '경기', '인천', '경상', '전라', '충청', '강원', '제주']

# 색상 설정
colors_fast = plt.cm.Reds(np.linspace(0.2, 0.8, len(target_months)))  # 급속 충전소 색상

# 날짜 변경: 원하는 이름으로 바꾸기
month_names = {
    '2020-12': '2020년',
    '2021-12': '2021년',
    '2022-12': '2022년',
    '2023-12': '2023년',
    '2024-12': '2024년'
}

# 그래프 설정
fig, ax = plt.subplots(figsize=(14, 10))

# 급속 충전소 누적값 초기화
bottom_values_fast = np.zeros(len(regions))  # 급속 충전소 초기 누적값

for idx, month in enumerate(target_months):
    # 급속 데이터 추출
    fast = df[(df['년월'] == month) & (df['충전속도'] == '급속')][regions].values[0]

    # 급속 충전소 표시
    ax.barh(regions, fast, left=bottom_values_fast, height=0.4, color=colors_fast[idx], label=f'급속 {month_names[month]}', alpha=0.8)

    # 누적 값 업데이트
    bottom_values_fast += fast

# 축 및 레이블 설정
ax.set_title('지역별 급속 전기차 충전소 수 (누적)', fontsize=16)
ax.set_xlabel('충전소 수', fontsize=13)
ax.set_ylabel('지역', fontsize=13)
ax.legend(title='년월', loc='upper right')  # 날짜 표시를 오른쪽 위로 이동
ax.grid(axis='x', linestyle='--', alpha=0.5)

plt.tight_layout()

# 저장 및 표시
filename = 'car7.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + ' saved')
plt.show()
