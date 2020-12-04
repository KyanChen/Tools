import os
import glob
import shutil
import numpy as np


def normalize_label(in_path, to_path, img_format, class_list):
    os.makedirs(to_path, exist_ok=True)
    img_file_list = glob.glob(in_path + '/*{}'.format(img_format))
    for img_file in img_file_list:
        bboxes = []
        with open(img_file.replace(img_format, 'txt'), 'r') as f:
            line = f.readline()
            while line != '' and line != '\n':
                data = line.replace('(', '').replace(')', '').strip().split(',')
                try:
                    data = [int(float(x)) for x in data]
                except:
                    pass
                data.insert(0, data.pop(-1))
                if data[0] in class_list:
                    bboxes.append(data)
                line = f.readline()
        bboxes = np.array(bboxes)
        to_img_file = to_path + '/' + os.path.basename(img_file)
        to_txt_file = to_img_file.replace(img_format, 'txt')
        if len(bboxes):
            np.savetxt(to_txt_file, bboxes, fmt='%d %d %d %d %d')
        else:
            with open(to_txt_file, 'w') as file:
                pass
        shutil.copyfile(img_file, to_img_file)


if __name__ == '__main__':
    in_path = r'F:\DataSet\NWPU VHR-10 dataset\positive image set'
    to_path = r'F:\DataSet\NWPU VHR-10 dataset\Normalized_Pos'
    img_format = 'jpg'
    class_list = [1, 2, 3]
    normalize_label(in_path, to_path, img_format, class_list)

