import glob
import os
import pandas as pd


def trans_to_csv(path):
    data_save = pd.DataFrame()
    data = pd.ExcelFile(path)
    table = data.parse(sheet_name=0).iloc[0:, :]
    # data_save = pd.concat((data_save, table), axis=0)
    table.to_csv(path.replace('xls', 'csv'), index=0)
    # with pd.ExcelWriter(r'挑选的数据/所有历史数据.xlsx', engine='xlsxwriter') as writer:
    #     data_save.to_excel(writer, index=False)


if __name__ == '__main__':
    path = r'G:\Coding\NLP\Code\Datasets'
    file_list = glob.glob(path + '/*.xls')
    for file in file_list:
        trans_to_csv(file)
