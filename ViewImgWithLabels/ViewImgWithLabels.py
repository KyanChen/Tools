import os
import cv2
import glob
import numpy as np


class ViewImg:
    def __init__(self, file_path, class_list, widthRatio, heightRatio, scalars, img_format='jpg'):
        assert os.path.exists(file_path), 'File path dose not exist!'
        self.img_list = glob.glob(file_path + '/*{}'.format(img_format))
        self.widthRatio = widthRatio
        self.heightRatio = heightRatio
        self.scalars = scalars
        self.class_list = class_list
        self.curFile = 0
        self.img_format = img_format
        self.bboxList = []

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

    def readTag(self):
        txt_file = self.img_list[self.curFile].replace(self.img_format, 'txt')
        if not os.path.exists(txt_file):
            file_to_read = open(txt_file, 'w')
            file_to_read.close()
        with open(txt_file, 'r') as file_to_read:
            lines = file_to_read.readline()  # 整行读取数据
            while lines:
                data = lines.strip().split()
                # dataToRead = list(map(int, data[1:]))
                class_id = self.class_list.index(data[0])
                try:
                    confidence, x1, y1, x2, y2 = [int(float(x)) for x in data[1:]]
                except Exception:
                    confidence = 1
                    x1, y1, x2, y2 = [int(float(x)) for x in data[1:]]

                data = [class_id, confidence, widthRatio * x1, heightRatio * y1, widthRatio * x2, heightRatio * y2]
                self.bboxList.append(data)
                lines = file_to_read.readline()

    def view(self):
        cv2.namedWindow('Window')
        cv2.moveWindow('Window', 300, 100)
        while self.curFile < len(self.img_list):
            self.bboxList.clear()
            img = cv2.imdecode(np.fromfile(self.img_list[self.curFile], dtype=np.uint8), cv2.IMREAD_COLOR)
            # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            width, height, _ = img.shape
            self.readTag()
            while True:
                cur_img = cv2.resize(img, (int(width * widthRatio), int(height * heightRatio)))
                print(str(self.curFile) + '/' + str(len(self.img_list)))

                for j in range(0, len(self.bboxList)):

                    class_id, confidence = self.bboxList[j][0:2]
                    x_1, y_1, x_2, y_2 = [int(x) for x in self.bboxList[j][2:]]
                    cur_img = cv2.rectangle(cur_img, (x_1, y_1), (x_2, y_2), self.scalars[class_id - 1], 2)
                    cv2.rectangle(cur_img, (x_1, y_1-20), (x_1+40, y_1), self.scalars[class_id - 1], -1)  # filled
                    cv2.putText(cur_img, '{}: {:.2f}'.format(self.class_list[class_id - 1], confidence),
                                (x_1, y_1-2), 0, 0.4,
                                [255, 255, 255],
                                thickness=1, lineType=cv2.FONT_HERSHEY_SIMPLEX)
                cv2.imshow("Window", cur_img)

                key_pressed = cv2.waitKey(1)
                a_pressed = [ord('a'), ord('A')]
                d_pressed = [ord('d'), ord('D')]
                if key_pressed in d_pressed:
                    self.curFile = self.curFile + 1
                    break
                elif key_pressed in a_pressed:
                    self.curFile = self.curFile - 1
                    if self.curFile < 0:
                        self.curFile = 0
                    break


if __name__ == '__main__':
    file_path = r'F:\DataSet\DIOR\JPEGImages-trainval'
    class_list = ['1', '2', '3']
    widthRatio = .5
    heightRatio = .5
    scalars = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (200, 5, 200)]

    get_label = ViewImg(file_path, class_list, widthRatio, heightRatio, scalars)
    get_label.view()

