import os
import glob
import numpy as np
import pandas as pd
import warnings

file_path = r'M:\Tiny_Ship\Exp\正样本\*.txt'
file_list = glob.glob(file_path)

n_bboxes = np.array([]).reshape([0, 3])
img_n = 0
for file_name in file_list:
    # # DOTA
    # bbox = np.loadtxt(file_name, dtype=float, converters={8: lambda x: x.decode() == 'ship'},
    # usecols=[0, 1, 4, 5, 8], ndmin=2)

    # # NWPU10
    # def converter(x):
    #     return x.decode().replace('(', '').replace(')', '')
    #
    # bbox = np.loadtxt(file_name, dtype=float, delimiter=',',
    #                   converters={0: converter, 1: converter,
    #                               2: converter, 3: converter,
    #                               4: lambda x: x.decode().replace(' ', '') == '2'},
    #                   ndmin=2)

    # # HRSC2016
    # bbox = np.loadtxt(file_name, dtype=float, ndmin=2)

    # # DIOR
    # with warnings.catch_warnings():
    #     warnings.simplefilter('ignore')
    #     bbox = np.loadtxt(file_name, dtype=float, ndmin=2)
    # if len(bbox):
    #     bbox = np.concatenate((bbox[:, 1:], bbox[:, 0:1]), axis=1)
    #     bbox[:, -1] = bbox[:, -1] == 2

    # # LEVIR
    # with warnings.catch_warnings():
    #     warnings.simplefilter('ignore')
    #     bbox = np.loadtxt(file_name, dtype=float, ndmin=2)
    #     bbox[:, 1::2] = np.clip(bbox[:, 1::2], 0, 800)
    #     bbox[:, 2::2] = np.clip(bbox[:, 2::2], 0, 600)
    # if len(bbox):
    #     bbox = np.concatenate((bbox[:, 1:], bbox[:, 0:1]), axis=1)
    #     bbox[:, -1] = bbox[:, -1] == 2

    # Levir-Ship
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        bbox = np.loadtxt(file_name, dtype=float, ndmin=2)
        bbox[:, 1::2] = np.clip(bbox[:, 1::2], 0, 256)
        bbox[:, 2::2] = np.clip(bbox[:, 2::2], 0, 256)
    if len(bbox):
        bbox = np.concatenate((bbox[:, 1:], bbox[:, 0:1]), axis=1)
        bbox[:, -1] = bbox[:, -1] == 0


    if len(bbox):
        bbox = bbox[bbox[:, 4] > 0]
        if len(bbox):
            w_h = bbox[:, 2:4] - bbox[:, 0:2]
            area = np.sqrt(np.prod(w_h, axis=1)).reshape(-1, 1)
            if any(area <= 2):
                print(f"error in {os.path.basename(file_name)}")
            n_bboxes = np.concatenate((n_bboxes, np.column_stack((w_h, area))), axis=0)
            img_n += 1

data_infos = pd.DataFrame(n_bboxes)
data_infos.to_csv(r"M:\Tiny_Ship\Exp\Levir-Ship\all_%d.csv" % img_n, index=False)
