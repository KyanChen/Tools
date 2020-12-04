import os
import glob

to_add_class = '3'


def add_annotations(in_path, to_path):
    def file_lines_to_list(path):
        with open(path) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        return content

    os.makedirs(to_path, exist_ok=True)
    file_list = glob.glob(in_path + '/*.txt')
    for file in file_list:
        line_list = file_lines_to_list(file)
        bbox_list = []
        for line in line_list:
            try:
                class_name, left, top, right, bottom = line.split()
            except:
                class_name, confidence, left, top, right, bottom = line.split()
            if class_name == to_add_class:
                bbox_list.append([class_name, left, top, right, bottom])
        with open(to_path + '/' + os.path.basename(file), 'a') as f:
            for box in bbox_list:
                string = ''
                for elem in box:
                    string += elem + ' '
                string += '\n'
                f.write(string)


if __name__ == '__main__':
    in_path = r'F:\DataSet\GF1_2\refined_data\B_3'
    out_path = r'F:\DataSet\GF1_2\refined_data\data'
    add_annotations(in_path, out_path)

