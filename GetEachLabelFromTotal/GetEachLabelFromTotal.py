import os
import glob
import shutil

txt_file = r'G:\Dataset\dataset_night\balloon.txt'
writer_path_label = r'G:\Dataset\dataset_night\dataset_night_416'
classes = ['balloon']
class_to_write = 0

class GetEachLabelFromTotal:

    def __init__(self):
        self.txt_file = txt_file
        self.writer_path_label = writer_path_label
        if not os.path.exists(self.writer_path_label):
            os.makedirs(self.writer_path_label)
        self.class_to_write = class_to_write

    @staticmethod
    def center_to_left(centerX, centerY, width, height):
        """
        Convert centerX, centerY, width, height to
        left, top, bottom, right form
        :return:
        """
        centerX, centerY, width, height = map(float, [centerX, centerY, width, height])
        left, top, bottom, right = int(centerX - width/2), int(centerY - height/2), \
            int(centerX + width/2), int(centerY + height/2)
        return left, top, bottom, right

    def delete_all_txt(self):
        txt_file_list = glob.glob(os.path.join(self.writer_path_label, '*.txt'))
        for file in txt_file_list:
            os.remove(file)

    def pair_txt_gt_predict(self, gt_path):
        """
        Make gt txt and predict txt pair
        :param img_path:
        :return:
        """
        gt_file_list = glob.glob(os.path.join(gt_path, '*.txt'))
        for gt_file in gt_file_list:
            gt_file = os.path.basename(gt_file)
            if not os.path.exists(os.path.join(writer_path_label, gt_file)):
                print(gt_file)
                with open(os.path.join(writer_path_label, gt_file), 'w') as f:
                    pass

    def get_label(self):
        assert os.path.exists(self.txt_file), 'txt_file dose not exist!'
        self.delete_all_txt()
        with open(self.txt_file, 'r') as f_reader:
            line = f_reader.readline()
            while line:
                name, confidence, centerX, centerY, width, height = line.strip().split()
                # left, top, bottom, right = self.center_to_left(centerX, centerY, width, height)
                left, top, bottom, right = map(lambda x: int(float(x)), [centerX, centerY, width, height])
                with open(os.path.join(self.writer_path_label, name+'.txt'), 'a') as f_writer:
                    f_writer.write('{0} {1} {2} {3} {4} {5}\n'.format(
                        classes[self.class_to_write], confidence, left, top, bottom, right))
                line = f_reader.readline()


if __name__ == '__main__':
    get_label = GetEachLabelFromTotal()
    get_label.get_label()
    get_label.pair_txt_gt_predict(r'G:\Dataset\dataset_night\dataset_night_done')

