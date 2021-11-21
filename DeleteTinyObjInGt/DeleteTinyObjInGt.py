import os
import glob
import tqdm


def refine(in_path, to_path):
    def file_lines_to_list(path):
        with open(path) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        return content

    os.makedirs(to_path, exist_ok=True)
    file_list = glob.glob(in_path + '/*.txt')
    for file in tqdm.tqdm(file_list):
        line_list = file_lines_to_list(file)
        bbox_list = []
        for line in line_list:
            try:
                class_name, left, top, right, bottom = line.split()
            except:
                class_name, confidence, left, top, right, bottom = line.split()
            w = float(right) - float(left)
            h = float(bottom) - float(top)
            if max(w, h) < 25:
                continue
            bbox_list.append([class_name, confidence, left, top, right, bottom])
        with open(to_path + '/' + os.path.basename(file), 'w') as f:
            for box in bbox_list:
                string = ''
                for elem in box:
                    string += elem + ' '
                string += '\n'
                f.write(string)


if __name__ == '__main__':
    in_path = r'G:\Coding\EfficientDet\EvalResults1020_select2'
    out_path = r'G:\Coding\EfficientDet\EvalResults1020_select2\no_tiny_obj'
    refine(in_path, out_path)

