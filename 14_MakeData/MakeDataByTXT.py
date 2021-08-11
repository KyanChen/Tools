import os
import glob
import pandas as pd
import numpy as np
from scipy import stats


def get_csv(file_path, data_dir):
    infos = {'img_path': [], 'label': []}
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            line = line.split()
            infos['img_path'].append(data_dir + '/' + line[0])
            labels = []
            for label in line[1:]:
                label = list(map(int, label.split(',')))
                labels.append(label)
            infos['label'].append(labels)
    data = pd.DataFrame(infos)
    data.to_csv(file_path.replace('.txt', '.csv'), index_label=False)


if __name__ == '__main__':
    data_dir = r'G:\Coding\pytorch-YOLOv4-master\datasets\coins'
    file_path = r'G:\Coding\pytorch-YOLOv4-master\datasets\train.txt'
    get_csv(file_path, data_dir)

