import os
import glob
import random
import shutil
import tqdm


def divide_samples(in_path, out_path, positive_rate=0.8, img_format='tiff'):
    img_file_list = glob.glob(in_path + '/*{}'.format(img_format))

    train_index = random.sample(range(0, len(img_file_list)), int(positive_rate * len(img_file_list)))
    val_index = set(range(0, len(img_file_list))) - set(train_index)
    lookup_dict = {'train': train_index, 'val': val_index}
    for key, value in lookup_dict.items():
        os.makedirs(out_path + '/{}'.format(key) + '/img', exist_ok=True)
        os.makedirs(out_path + '/{}'.format(key) + '/label', exist_ok=True)
        for i in tqdm.tqdm(value):
            img_file = img_file_list[i]
            # txt_file = img_file.replace(img_format, 'txt')
            label_file = img_file.replace('img', 'label')
            to_img_file = out_path + '/{}/'.format(key) + 'img/' + os.path.basename(img_file)
            # to_txt_file = to_img_file.replace(img_format, 'txt')
            to_label_file = to_img_file.replace('img', 'label')
            shutil.copyfile(img_file, to_img_file)
            shutil.copyfile(label_file, to_label_file)


if __name__ == '__main__':
    in_path = r'J:\20200923-建筑提取数据集\InriaAerialImageDataset\train\pieces\img'
    out_path = r'J:\20200923-建筑提取数据集\InriaAerialImageDataset\train\pieces\total'
    divide_samples(in_path, out_path)

