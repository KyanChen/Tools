import os
import glob
import random
import shutil
import tqdm


def divide_samples(in_path, out_path, positive_rate=0.7, img_format='jpg'):
    img_file_list = glob.glob(in_path + '/*{}'.format(img_format))

    train_index = random.sample(range(0, len(img_file_list)), int(positive_rate * len(img_file_list)))
    val_index = set(range(0, len(img_file_list))) - set(train_index)
    lookup_dict = {'train': train_index, 'val': val_index}
    for key, value in lookup_dict.items():
        os.makedirs(out_path + '/{}'.format(key), exist_ok=True)
        for i in tqdm.tqdm(value):
            img_file = img_file_list[i]
            txt_file = img_file.replace(img_format, 'txt')
            to_img_file = out_path + '/{}/'.format(key) + os.path.basename(img_file)
            to_txt_file = to_img_file.replace(img_format, 'txt')
            shutil.copyfile(img_file, to_img_file)
            shutil.copyfile(txt_file, to_txt_file)


if __name__ == '__main__':
    in_path = r'F:\DataSet\GF1_2\total_data'
    out_path = r'F:\DataSet\GF1_2\total_data'
    divide_samples(in_path, out_path)

