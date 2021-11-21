import sys
import os
import glob
import xml.etree.ElementTree as T

class_list = ['face', 'face_mask']
xml_path = r'L:\Detection\HRSC2016\HRSC2016\HRSC\HRSC2016\FullDataSet\Annotations'
save_txt_path = r'L:\Detection\HRSC2016\HRSC2016\HRSC\HRSC2016\FullDataSet\Annotations_Txt'


def get_txt_files(xml_path, save_txt_path, class_list):
    os.makedirs(save_txt_path, exist_ok=True)
    xml_file_list = glob.glob(xml_path + '/*.xml')
    assert len(xml_file_list), "Error: no .xml files found in ground-truth"
    for xml_file in xml_file_list:
        with open(save_txt_path + '/' + os.path.basename(xml_file).replace(".xml", ".txt"), "w") as new_f:
            root = T.parse(xml_file).getroot().find('HRSC_Objects')
            for obj in root.findall('HRSC_Object'):

                left = obj.find('box_xmin').text
                top = obj.find('box_ymin').text
                right = obj.find('box_xmax').text
                bottom = obj.find('box_ymax').text
                new_f.write(left + " " + top + " " + right + " " + bottom + ' 1' + '\n')

                # obj_name = obj.find('name').text
                # if obj_name in class_list:
                #     obj_name = class_list.index(obj_name)
                #     bndbox = obj.find('bndbox')
                #     left = bndbox.find('xmin').text
                #     top = bndbox.find('ymin').text
                #     right = bndbox.find('xmax').text
                #     bottom = bndbox.find('ymax').text
                #     new_f.write(repr(obj_name) + " " + left + " " + top + " " + right + " " + bottom + '\n')
    print("Conversion completed!")


if __name__ == '__main__':
    get_txt_files(xml_path, save_txt_path, class_list)