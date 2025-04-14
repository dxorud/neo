import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'NanumBarunGothic'

filename = 'tips.csv'

myframe = pd.read_csv(filename, encoding='utf-8')
print('head() 메소드 결과')
print(myframe.head())
print('-' * 50)

print('info() 메소드 결과')
print(myframe.info())
print('-' * 50)

mycolor = ['r', 'g']
label = ['Female', 'Male']

cnt = 0

for finditem in label:
    xdata = myframe[myframe['sex'] == finditem]['total_bill']
    ydata = myframe[myframe['sex'] == finditem]['tip']
    plt.plot(xdata, ydata, label=finditem, color=mycolor[cnt], marker='o', linestyle='None')
    cnt += 1

    plt.legend(loc=2)
    plt.grid(True)
    plt.xlabel('결제 총액')
    plt.ylabel('팁 비용')
    plt.title('결제 총액과 팁 비용의 산점도')
    plt.show()

    filename = 'Ex_p239_08.png'
    plt.savefig(filename, dpi=400, bbox_inches='tight')
    print(filename + ' saved')
    plt.show()
