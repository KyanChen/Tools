import numpy as np
import pandas as pd
import os

csv_file = r'M:\Tiny_Ship\Exp\Levir-Ship\all_8074.csv'
data = pd.read_csv(csv_file)
print("samples:" + repr(len(data)))
area = np.array(data.iloc[:, 2])
print(f'min_area:{np.min(area)} max_area:{np.max(area)} mean_area:{np.mean(area)}')
