import os
import glob
import tqdm
import shutil


IMG_PATH_DIR = r"K:\Positive_Patches\待确认"
SAVE_PATH = r'K:\Positive_Patches'


def get_pos(file_list, save_path):
    for txt_file in tqdm.tqdm(file_list):
        if os.path.getsize(txt_file) > 0:
            to_parent_path = save_path + '/' + os.path.basename(os.path.dirname(txt_file))
            os.makedirs(to_parent_path, exist_ok=True)
            shutil.copy(txt_file, to_parent_path + '/' + os.path.basename(txt_file))
            shutil.copy(txt_file.replace('.txt', '.tiff'), to_parent_path + '/' + os.path.basename(txt_file).replace('.txt', '.tiff'))


def main():
    dir_list = glob.glob(IMG_PATH_DIR + '/*')
    assert len(dir_list), IMG_PATH_DIR + ' Empty!'
    if os.path.isfile(dir_list[int(len(dir_list) / 2)]):
        file_list = [x for x in dir_list if x.endswith('txt')]
        get_pos(file_list, SAVE_PATH)
    else:
        dir_list = [x for x in dir_list if os.path.isdir(x)]
        for dir in dir_list:
            file_list = glob.glob(dir + '/*.txt')
            get_pos(file_list, SAVE_PATH)


if __name__ == '__main__':
    main()


