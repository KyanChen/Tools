import json
import os
import shutil
import numpy as np

json_file = r'F:\OneDrive\MyWork\Kaikeba\20201022公共场景下的口罩实时监测4,5\code\PyTorch-YOLOv3-master\data\mydata\ParserJSON\instances_val2017.json'
out_path = r'F:\OneDrive\MyWork\Kaikeba\20201022公共场景下的口罩实时监测4,5\code\PyTorch-YOLOv3-master\data\mydata\ParserJSON\OutputTXT'

if os.path.exists(out_path):
    shutil.rmtree(out_path)
os.makedirs(out_path, exist_ok=True)

with open(json_file, 'r') as f:
    data = json.load(f)
annotations = data['annotations']
for annotation in annotations:
    with open(out_path + '/%012d.txt' % annotation['image_id'], 'a') as f:
        str = repr(annotation['category_id']) + ' '
        bboxes = np.array(annotation['bbox'])
        bboxes[2:] = bboxes[:2] + bboxes[2:]
        str += ' '.join(map(repr, bboxes))
        str += '\n'
        f.write(str)

