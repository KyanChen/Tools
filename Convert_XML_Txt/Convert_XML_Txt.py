import sys
import os
import glob
import xml.etree.ElementTree as T


# change directory to the one with the files to be changed
xml_path = r'/Users/keyanchen/Files/Dataset/704/ship_detection_online/Annotations_new'
save_path_txt = r'/Users/keyanchen/Files/Dataset/704/ship_detection_online/Txt'

# old files (xml format) will be moved to a "backup" folder
# create the backup dir if it doesn't exist already
if not os.path.exists(save_path_txt):
    os.makedirs(save_path_txt)

# create VOC format files
xml_list = glob.glob(os.path.join(xml_path, '*.xml'))
assert len(xml_list), "Error: no .xml files found in ground-truth"

for tmp_file in xml_list:
  # 1. create new file (VOC format)
  with open(os.path.join(save_path_txt, os.path.basename(tmp_file).replace(".xml", ".txt")), "a") as new_f:
    root = T.parse(tmp_file).getroot()
    for obj in root.findall('object'):
      obj_name = obj.find('name').text
      bndbox = obj.find('bndbox')
      left = bndbox.find('xmin').text
      top = bndbox.find('ymin').text
      right = bndbox.find('xmax').text
      bottom = bndbox.find('ymax').text
      new_f.write(obj_name + " " + left + " " + top + " " + right + " " + bottom + '\n')

print("Conversion completed!")
