import pandas as pd
import matplotlib.pyplot as plt

file_path = "gyeonggi_2040.csv" 
df = pd.read_csv(file_path)

df.columns = df.columns.str.strip()

target_region = df[df['sigungu'] == '고양시 덕양구']

years = [str(y) for y in range(2022, 2041)]
values = target_region[years].iloc[0]

plt.figure(figsize=(12, 6))
plt.plot(years, values, marker='o', linestyle='-', linewidth=2)

plt.rcParams['font.family'] = 'Malgun Gothic' 

plt.title('고양시 덕양구 전기차 등록대수 예측 (2022~2040)', fontsize=16)
plt.xlabel('연도')
plt.ylabel('전기차 등록대수')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

filename = 'gyeonggi.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + ' saved')
plt.show()
