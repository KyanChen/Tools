import glob
import os
import zipfile
import tqdm

file_path = r'I:\GF\Patches'
out_path = r'I:\GF\Patches'

file_path_list = glob.glob(f"{file_path}/GF*")
file_path_list.sort(reverse=True)


def get_zip_file(input_path, result):
    """
    对目录进行深度优先遍历
    :param input_path:
    :param result:
    :return:
    """
    files = os.listdir(input_path)
    for file in files:
        if os.path.isdir(input_path + '/' + file):
            get_zip_file(input_path + '/' + file, result)
        else:
            result.append(input_path + '/' + file)


def zip_file_path(input_path, output_path, output_name):
    """
    压缩文件
    :param input_path: 压缩的文件夹路径
    :param output_path: 解压（输出）的路径
    :param output_name: 压缩包名称
    :return:
    """
    f = zipfile.ZipFile(output_path + '/' + output_name, 'w', zipfile.ZIP_DEFLATED)
    filelists = []
    get_zip_file(input_path, filelists)
    for file in filelists:
        f.write(file)
        # 调用了close方法才会保证完成压缩
    f.close()
    return output_path + "/" + output_name


if __name__ == '__main__':
    for file in tqdm.tqdm(file_path_list):
        zip_file_path(file, out_path, os.path.basename(file) + '.zip')



