import glob
import pandas as pd
import os


def get_all_data(path_list):
    data_save = pd.DataFrame()
    for path in path_list:
        data = pd.read_csv(path)
        table = data.iloc[:, 1:14]
        table = table.dropna(axis=0, how='all')
        data_save = pd.concat((data_save, table), axis=0)
    data_save.to_csv(os.path.dirname(path_list[0]) + '/所有数据.csv', index=0)
    with pd.ExcelWriter(os.path.dirname(path_list[0]) + '/所有数据.xlsx', engine='xlsxwriter') as writer:
        data_save.to_excel(writer, index=False)


if __name__ == '__main__':
    file_path = r'G:\Coding\NLP\Code\Datasets'
    file_list = glob.glob(file_path + "/*.csv")
    get_all_data(file_list)
    table = pd.read_csv(r'G:\Coding\NLP\Code\Datasets\所有数据.csv')
    pass