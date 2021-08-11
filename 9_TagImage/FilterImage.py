import cv2
import os
import shutil
from skimage import io
import glob
import numpy as np
import copy

in_path = r"I:\GF\temp_uncompress"
img_format = 'jpg'

tar_path = r'J:\GF1_GF6'
tar_save_path = r'J:\20210117_GF1_GF6数据'


class FilterImage:
    def __init__(self, in_path, img_format):
        self.file_list = self._get_file([in_path], img_format)

    def _get_file(self, in_path_list, img_format):
        file_list = []
        for file in in_path_list:
            if os.path.isdir(file):
                files = glob.glob(file + '/*')
                file_list.extend(self._get_file(files, img_format))
            else:
                if file.split('.')[-1] == img_format and 'thumb' not in file and '-' not in file:
                    file_list += [file]
        return file_list

    def _move_data(self, file_name):
        shutil.rmtree(os.path.dirname(file_name))
        tar_name = os.path.basename(os.path.dirname(file_name)) + '.tar.gz'
        shutil.move(tar_path + f'/{tar_name}', tar_save_path + f'/陆地/{tar_name}')

    def _save_data(self, file_name):
        tar_name = os.path.basename(os.path.dirname(file_name)) + '.tar.gz'
        try:
            shutil.move(tar_path + f'/{tar_name}', tar_save_path + f'/海上/{tar_name}')
        except FileNotFoundError:
            pass

    def _remove_data(self, file_name):
        shutil.rmtree(os.path.dirname(file_name))
        tar_name = os.path.basename(os.path.dirname(file_name)) + '.tar.gz'
        os.remove(tar_path + f'/{tar_name}')

    def run(self):
        idx = 0
        while idx < len(self.file_list):
            self.file_list = self._get_file([in_path], img_format)

            img = copy.copy(io.imread(self.file_list[idx])[:, :, ::-1])
            # (b, g, r) = cv2.split(img)
            # bH = cv2.equalizeHist(b)
            # gH = cv2.equalizeHist(g)
            # rH = cv2.equalizeHist(r)
            # # 合并每一个通道
            # result = cv2.merge((bH, gH, rH))
            cv2.namedWindow(f"img", cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(f"img", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.putText(img, f"{idx}", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 5)
            cv2.putText(img, f"Y:Sea,R:Cloud,M:Land", (20, 500), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 5)
            cv2.imshow(f"img", img)
            while True:
                key_pressed = cv2.waitKey(1)
                f_pressed = [ord('D'), ord('d')]
                b_pressed = [ord('A'), ord('a')]
                m_pressed = [ord('M'), ord('m')]
                r_pressed = [ord('R'), ord('r')]
                y_pressed = [ord('Y'), ord('y')]
                if key_pressed in r_pressed:
                    self._remove_data(self.file_list[idx])
                    break
                elif key_pressed in m_pressed:
                    self._move_data(self.file_list[idx])
                    break
                elif key_pressed in y_pressed:
                    self._save_data(self.file_list[idx])
                    idx += 1
                    if idx >= len(self.file_list):
                        idx = len(self.file_list) - 1
                    break
                elif key_pressed in f_pressed:
                    idx += 1
                    if idx >= len(self.file_list):
                        idx = len(self.file_list) - 1
                    break
                elif key_pressed in b_pressed:
                    idx -= 1
                    if idx < 0:
                        idx = 0
                    break
                elif key_pressed == 27:
                    cv2.destroyAllWindows()


def main():
    filterImg = FilterImage(in_path, img_format)
    filterImg.run()


if __name__ == '__main__':
    main()








