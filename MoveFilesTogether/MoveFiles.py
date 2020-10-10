import os
import shutil
import glob
import tqdm


def move_files(parent_path, to_path):
    os.makedirs(to_path, exist_ok=True)
    files_list = glob.glob(parent_path + '/*/*')
    for elem in tqdm.tqdm(files_list):
        to_file = to_path + '/' + os.path.basename(elem)
        shutil.copyfile(elem, to_file)


if __name__ == '__main__':
    parent_path = r'F:\DataSet\GF1_2\test_data'
    to_path = r'F:\DataSet\GF1_2\total_data'
    move_files(parent_path, to_path)

