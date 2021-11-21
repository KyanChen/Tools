import numpy as np
import glob
import os
import tqdm
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif'] = ['FangSong', 'SimHei', 'Times New Roman']
mpl.rcParams['axes.unicode_minus'] = False  # 正常显示负号
# darkgrid white dark whitegrid  ticks
sns.set_theme(style="darkgrid")
# sns.set(font=['SimHei', 'Times New Roman'])
sns.set(font_scale=1.5)

current_palette = sns.color_palette()


dota = r'M:\Work\Exp\DOTA\ship_total_all.csv'
levir = r'M:\Work\Exp\Levir\ship_total_all.csv'
nwpu = r'M:\Work\Exp\NWPU10\all_57.csv'
hrsc = r'M:\Work\Exp\HRSC2016\all_1055.csv'
dior = r'M:\Work\Exp\DIOR\all_2698.csv'
levir_ship = r'M:\Work\Exp\Levir-Ship\all_8074.csv'

file_list = [dota, levir, nwpu, hrsc, dior, levir_ship]
area_list = []
for file_name in file_list:
    data_frame = pd.read_csv(file_name)
    area = data_frame.iloc[:, 2]
    area = np.array(area)
    area_list += [area]

"""
绘制直方图
data:必选参数，绘图数据
bins:直方图的长条形数目，可选项，默认为10
normed:是否将得到的直方图向量归一化，可选项，默认为0，代表不归一化，显示频数。normed=1，表示归一化，显示频率。
facecolor:长条形的颜色
edgecolor:长条形边框的颜色
alpha:透明度
"""
i = 0

f, ax = plt.subplots(figsize=(20, 10))
sns.despine(f)  # 移除顶部和右侧脊柱

sns.histplot(
    [area_list[i], area_list[-1]], common_norm=False, stat='probability', bins=100, binrange=[0, 150],
    palette=sns.color_palette(['#33a02c','#1f78b4'])
)
ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
# ax.set_xticks([0, 50, 100])
legends = ['DOTA', 'Levir', 'NWPU VHR-10', 'HRSC2016', 'DIOR',  'Levir-Ship']
ax.legend((legends[-1], legends[i]), loc='upper right', frameon=False)
# 显示横轴标签
plt.xlabel("AS", weight='bold')
# 显示纵轴标签
plt.ylabel("Probability", weight='bold')
# 显示图标题
plt.title(f"Ship Distribution for {legends[i]} and {legends[-1]}", weight='bold')
# plt.show()
plt.savefig(r'M:\Work\Exp\%d.png' % i)

