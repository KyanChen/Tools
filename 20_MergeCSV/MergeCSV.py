import os
import glob
import random

import pandas as pd
import cv2
import tqdm
import numpy as np

csv_file_names = [
    r'M:\Tiny_Ship\Exp\Levir\train_1019.csv',
    r'M:\Tiny_Ship\Exp\Levir\val_475.csv'
]

data_annotation = []
for file_name in csv_file_names:
    data_annotation.append(pd.read_csv(file_name))

data_annotation = pd.concat(data_annotation)
# data_annotation = data_annotation.sample(frac=1).reset_index(drop=True)

writer_name = os.path.dirname(csv_file_names[0]) + '/ship_total_all.csv'
data_annotation.to_csv(writer_name, index=False)
print(os.path.basename(writer_name) + ' file saves successfully!')

# val_data = data_annotation.sample(frac=0.1, replace=False)
# val_data = val_data.reset_index(drop=True)
# writer_name = os.path.dirname(csv_file_names[0]) + '/ship_train_total_all_val.csv'
# val_data.to_csv(writer_name, index_label=False)