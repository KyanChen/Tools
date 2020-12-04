import cv2
import gdal
import os
import shutil
import numpy as np
import glob
import copy

# Esc取消一个标注
# D、A分别对应下一张图像和上一张图像

IMG_PATH_DIR = r"F:\OneDrive\MyWork\Kaikeba\20201022公共场景下的口罩实时监测4,5\code\PyTorch-YOLOv3-master\data\custom\images"
# CLASSES = ['1', '2', '3']
CLASSES = [repr(x) for x in range(0, 90)]
CURRENT_ANNOTATE_CLASS = '8'
WIDTH_ZOOM = 1
HEIGHT_ZOOM = 1
IMG_FORMAT = 'jpg'
MODE = 'normal'

# SCALARS = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (200, 5, 200)]
SCALARS = [(x, x, x) for x in range(0, 255, 2)]


class AnnotateImage:

    def __init__(self, path_dir, mode='gdal'):
        self.path_dir = path_dir
        self.file_list = self.get_file_list(self.path_dir)
        assert len(self.file_list), path_dir + ' No Data!'
        self.dep_file = path_dir + '/temp'
        os.makedirs(self.dep_file, exist_ok=True)
        self.mode = mode
        self.cur_file_id = self.read_resume_file_id(self.dep_file)
        self.cur_file_id = np.clip(self.cur_file_id, a_min=0, a_max=len(self.file_list)-1)
        self.bbox_list = []
        self.flag_is_draw_finished = True
        self.temp_draw_box = [0, 0, 0, 0]
        self.cur_XY = [0, 0]
        self.isDrawFinished = True

    @staticmethod
    def get_file_list(path):
        file_list = glob.glob(path + '/*.%s' % IMG_FORMAT)
        file_list.sort()
        return file_list

    @staticmethod
    def read_resume_file_id(path):
        path += '/resume_file_id.txt'
        if os.path.exists(path):
            with open(path, 'r') as file:
                return int(file.readline())
        else:
            return 0

    def write_resume_file_id(self, resume_file_id):
        path = self.dep_file + '/resume_file_id.txt'
        with open(path, 'w') as file:
            file.write(repr(resume_file_id))

    @staticmethod
    def read_annotations(img_file, size_infos):
        txt_file = img_file.replace(IMG_FORMAT, 'txt')
        bbox_list = []
        if not os.path.exists(txt_file):
            with open(txt_file, 'w', encoding='utf-8') as f_read:
                pass
        else:
            with open(txt_file, 'r', encoding='utf-8') as f_read:
                lines = f_read.readlines()
                datas = [x.strip().split() for x in lines]
                datas = [x for x in datas if len(x) > 0]
                for data in datas:
                    data[0] = CLASSES.index(data[0])
                    data = list(map(int, map(float, data)))
                    data = np.array(data)
                    data[1::2] = data[1::2] * WIDTH_ZOOM
                    data[2::2] = data[2::2] * HEIGHT_ZOOM
                    data = list(map(int, data))
                    bbox_list.append(data)
        return bbox_list

    def save_annotations(self, img_file):
        txt_file = img_file.replace(IMG_FORMAT, 'txt')
        with open(txt_file, 'w') as f_write:
            for box in self.bbox_list:
                box = np.array(box)
                box[1::2] = box[1::2] / WIDTH_ZOOM
                box[2::2] = box[2::2] / HEIGHT_ZOOM
                box = list(map(int, box))
                line = CLASSES[box[0]] + ''.join([' ' + repr(x) for x in box[1:]])
                line += '\n'
                f_write.write(line)

    # 创建回调函数
    def draw_rectangle(self, event, x, y, flags, param):
        self.cur_XY = [x, y]
        if event == cv2.EVENT_LBUTTONDOWN:
            self.flag_is_draw_finished = False
            self.temp_draw_box[0:2] = [x, y]
        # 当鼠标左键按下并移动是绘制图形。event可以查看移动，flag查看是否按下
        elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            # self.flag_is_draw_finished = False
            self.temp_draw_box[2:] = [x, y]
        elif event == cv2.EVENT_LBUTTONUP:
            self.flag_is_draw_finished = True
            self.temp_draw_box[2:] = [x, y]
            left, top, right, bottom = self.refine_corners(*self.temp_draw_box)
            t = CLASSES.index(CURRENT_ANNOTATE_CLASS)
            self.bbox_list.append([CLASSES.index(CURRENT_ANNOTATE_CLASS), left, top, right, bottom])

    @staticmethod
    def refine_corners(x_1, y_1, x_2, y_2):
        if x_1 < x_2:
            if y_1 < y_2:
                left, top, right, bottom = x_1, y_1, x_2, y_2
            elif y_1 > y_2:
                left, top, right, bottom = x_1, y_2, x_2, y_1
        elif x_1 > x_2:
            if y_1 < y_2:
                left, top, right, bottom = x_2, y_1, x_1, y_2
            elif y_1 > y_2:
                left, top, right, bottom = x_2, y_2, x_1, y_1
        return left, top, right, bottom

    @staticmethod
    def read_img(file, mode):
        if mode == 'normal':
            img = cv2.imread(file, cv2.IMREAD_COLOR)
            if img is None:
                img = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_COLOR)
                # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            origin_height, origin_width, _ = img.shape
            present_width, present_height = int(origin_width * WIDTH_ZOOM), int(origin_height * HEIGHT_ZOOM)
            img = cv2.resize(img, (present_width, present_height), interpolation=cv2.INTER_LINEAR)
        elif mode == 'gdal':
            data_set = gdal.Open(file)
            origin_width = data_set.RasterXSize
            origin_height = data_set.RasterYSize
            origin_count = data_set.RasterCount
            present_width, present_height = int(origin_width * WIDTH_ZOOM), int(origin_height * HEIGHT_ZOOM)
            # m = data_set.ReadAsArray(0, 0, origin_width, origin_height)
            img_data = np.zeros((origin_count, present_height, present_width), dtype=np.uint16)
            data_set.ReadAsArray(0, 0, origin_width, origin_height,
                                 img_data, present_width, present_height,
                                 buf_type=gdal.GDT_UInt16, resample_alg=gdal.GRIORA_Bilinear)
            img_data = img_data[:3][::-1]
            img_data = np.transpose(img_data, (1, 2, 0))
            min_value, max_value = np.min(img_data), np.max(img_data)
            # 截断部分值
            min_value = 0 + 0.01 * min_value
            max_value = max_value - (max_value - min_value) * 0.01
            img_data = (img_data.astype(np.float32) - min_value) / (max_value - min_value + 1e-10)
            img = (np.clip(img_data, a_min=0, a_max=1) * 255).astype(np.uint8)
        return img, {'origin_width': origin_width,
                     'origin_height': origin_height,
                     'present_width': present_width,
                     'present_height': present_height}

    def run(self):
        cv2.namedWindow('Annotation_Window')
        cv2.moveWindow('Annotation_Window', 300, 100)
        while self.cur_file_id < len(self.file_list):
            img_src, size_infos = self.read_img(self.file_list[self.cur_file_id], mode=self.mode)
            self.bbox_list = self.read_annotations(self.file_list[self.cur_file_id], size_infos)
            # 绑定事件
            cv2.setMouseCallback('Annotation_Window', self.draw_rectangle)
            while True:
                img = img_src.copy()
                print(str(self.cur_file_id) + '/' + str(len(self.file_list)))
                for bbox in self.bbox_list:
                    class_id, left, top, right, bottom = bbox
                    cv2.rectangle(img, (left, top), (right, bottom), SCALARS[class_id], 2)
                    cv2.putText(img, CLASSES[class_id], (left, top), cv2.FONT_HERSHEY_COMPLEX, 0.8, SCALARS[class_id], 1)
                if not self.flag_is_draw_finished:
                    cv2.rectangle(img, tuple(self.temp_draw_box[:2]), tuple(self.temp_draw_box[2:]), (255, 255, 255), thickness=1)

                cv2.line(img, (self.cur_XY[0], 0), (self.cur_XY[0], size_infos['present_height']), (255, 255, 255), 1)
                cv2.line(img, (0, self.cur_XY[1]), (size_infos['present_width'], self.cur_XY[1]), (255, 255, 255), 1)

                cv2.imshow("Annotation_Window", img)
                key_pressed = cv2.waitKey(1)
                a_pressed = [ord('a'), ord('A')]
                d_pressed = [ord('d'), ord('D')]
                undo_pressed = [27]
                if key_pressed in d_pressed:
                    self.save_annotations(self.file_list[self.cur_file_id])
                    self.cur_file_id += 1
                    self.write_resume_file_id(self.cur_file_id)
                    break
                elif key_pressed in a_pressed:
                    self.save_annotations(self.file_list[self.cur_file_id])
                    self.cur_file_id -= 1
                    self.cur_file_id = np.max(0, self.cur_file_id)
                    self.write_resume_file_id(self.cur_file_id)
                    break
                elif key_pressed in undo_pressed:
                    if len(self.bbox_list):
                        self.bbox_list.pop()
                    else:
                        continue


def main():
    annotator = AnnotateImage(IMG_PATH_DIR, MODE)
    annotator.run()


if __name__ == '__main__':
    main()


