import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

file_path = '한국전력공사_지역별 전기차 충전소 현황정보.csv'
df = pd.read_csv(file_path)
plt.rcParams['font.family'] = 'NanumBarunGothic'

print(df.head())

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '#FF6347', '#8A2BE2', '#3CB371']

plt.figure(figsize=(12, 8))

for i, region in enumerate(df['지역']):
    plt.plot(df.columns[1:], df.iloc[i].values[1:], label=region, color=colors[i % len(colors)])

plt.title('지역별 전기차 충전소 수 (2016-2023)', fontsize=16)
plt.xlabel('연도', fontsize=14)
plt.ylabel('충전소 수 (개)', fontsize=14)
plt.legend(title='지역', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()


filename = 'car2.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + ' saved')
plt.show()
