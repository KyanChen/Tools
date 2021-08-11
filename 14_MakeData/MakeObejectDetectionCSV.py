import os
import glob
import pandas as pd
import numpy as np
from scipy import stats


def get_csv(img_path, phase_list, img_format='jpg'):
    for phase in phase_list:
        img_files = glob.glob(img_path + f'/{phase}' + f'/*[0-9].{img_format}')
        infos = {'img_path': [], 'main_label': [], 'label': []}
        for img_file in img_files:
            txt_file = img_file.replace(img_format, 'txt')
            infos['img_path'].append(os.path.basename(img_file))
            labels = np.loadtxt(txt_file, int, ndmin=2)
            main_label, _ = stats.mode(labels, axis=0)
            if len(main_label) == 0:
                main_label = -1
            else:
                main_label = main_label[0][0]
            infos['main_label'].append(main_label)
            label_list = []
            for label in labels:
                label_list.append(list(label))
            infos['label'].append(label_list)
        data = pd.DataFrame(infos)
        data.to_csv(img_path + f'/{phase}.csv', index_label=False)


def sample_data(csv_path, phase_list, frac=0.1):
    for phase in phase_list:
        data_total = pd.read_csv(csv_path + f'/{phase}.csv')
        data_samples = pd.DataFrame()
        for category in range(0, 20):
            data_category = data_total[data_total['main_label'] == category].reset_index(drop=True)
            print(f'{category}:{len(data_category)}')
            data_sample = data_category.sample(frac=frac, replace=False).reset_index(drop=True)
            data_samples = data_samples.append(data_sample, ignore_index=True)
        for idx, d in data_samples.iterrows():
            data_samples.iloc[idx, 0] = r'I:\datadet\DIOR' + '/' + phase + '/' + d['img_path']
        data_samples.to_csv(csv_path + f'/{phase}_sample.csv', index_label=False)


if __name__ == '__main__':
    phase_list = ['train', 'val', 'test']
    # phase_list = ['test']
    # img_path = r'I:\目标检测数据及预训练模型\DIOR'
    # get_csv(img_path, phase_list)
    csv_path = r'I:\datadet\DIOR'
    sample_data(csv_path, phase_list, frac=0.05)

