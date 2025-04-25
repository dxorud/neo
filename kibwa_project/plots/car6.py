import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

# 폰트 설정
plt.rcParams['font.family'] = 'NanumBarunGothic'
mpl.rcParams['axes.unicode_minus'] = False

# CSV 파일 로드
df = pd.read_csv('지역별_전기차_충전기_구축현황(누적).csv', encoding='utf-8')
df.columns = df.columns.str.strip()

# 사용할 년월 및 지역 리스트
target_months = ['2020-12', '2021-12', '2022-12', '2023-12', '2024-12']
regions = ['서울','경기','인천','경상','전라','충청','강원','제주']

# 1) 완속 데이터만 추출해서, 각 지역별 총합 계산
df_slow = df[df['충전속도']=='완속'].set_index('년월').loc[target_months, regions]
totals = df_slow.sum(axis=0)                            # 각 지역별 총합
sorted_regions = totals.sort_values(ascending=False).index.tolist()

# 2) 누적 막대그래프를 위해 재정렬된 순서에 맞춰 데이터를 준비
bottom = np.zeros(len(sorted_regions))
colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(target_months)))
month_names = {'2020-12':'2020년','2021-12':'2021년','2022-12':'2022년','2023-12':'2023년','2024-12':'2024년'}

fig, ax = plt.subplots(figsize=(14,10))
for idx, m in enumerate(target_months):
    values = df_slow.loc[m, sorted_regions].values
    ax.barh(sorted_regions, values, left=bottom, height=0.6,
            color=colors[idx], label=month_names[m], alpha=0.8)
    bottom += values

# 3) 축, 레이블, 레전드 설정
ax.set_title('지역별 전기차 완속 충전소 수 (연도별 누적, 총합 내림차순)', fontsize=16)
ax.set_xlabel('충전소 수', fontsize=13)
ax.set_ylabel('지역', fontsize=13)
ax.legend(title='년월', loc='upper right')
ax.grid(axis='x', linestyle='--', alpha=0.5)

plt.tight_layout()

filename = 'car6-1.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + ' saved')
plt.show()
