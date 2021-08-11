import glob
import os


def get_file(in_path, relative_path):
    img_file_list = glob.glob(in_path + '/*jpg')
    img_file_list = [x.replace(relative_path + '\\', '').replace('\\', '/') + '\n' for x in img_file_list]
    with open(in_path + '/../val.txt', 'w') as f:
        f.writelines(img_file_list)


if __name__ == '__main__':
    in_path = r'G:\Coding\YOLOv4_Refine\dataset\train_data'
    relative_path = r'F:\OneDrive\MyWork\Kaikeba\20201022公共场景下的口罩实时监测4,5\code\PyTorch-YOLOv3-master'
    get_file(in_path, relative_path)

