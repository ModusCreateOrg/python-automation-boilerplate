from os import path, listdir

from gherkin.token_scanner import TokenScanner
from gherkin.parser import Parser


def data_table_vertical_converter(data_table_raw: str):
    data_table_list = data_table_raw.split("|")
    data_table_list = [elem.strip() for elem in data_table_list]
    data_table_list = list(filter(lambda elem: elem != "", data_table_list))
    return {data_table_list[i]: data_table_list[i + 1] for i in range(0, len(data_table_list) - 1, 2)}


def data_table_horizontal_converter(data_table_raw: str):
    data_table_rows = data_table_raw.split("\n")
    data_table_rows = [i for i in data_table_rows if i]
    data_table_header = data_table_rows[0].split('|')
    data_table_header = [i.strip() for i in data_table_header if i]
    data_table = {data_table_header[i]: [] for i in range(0, len(data_table_header))}

    for i in range(1, len(data_table_header)):
        data_table_row = data_table_rows[i].split('|')
        data_table_row = [i.strip() for i in data_table_row if i]
        for j in range(0, len(data_table_header)):
            data_table[data_table_header[j]].append(data_table_row[j])


def get_feature(file_path: str):
    """ Read and parse given feature file"""
    print('Reading feature file ', file_path)
    file_obj = open(file_path, "r")
    steam = file_obj.read()
    parser = Parser()
    return parser.parse(TokenScanner(steam))


def get_feature_files_path(export_tests_path: str):
    tests_abs_path = path.abspath(export_tests_path)
    if path.isfile(tests_abs_path):
        return [tests_abs_path]
    files_path = [path.join(tests_abs_path, f) for f in listdir(tests_abs_path) if
                  path.isfile(path.join(tests_abs_path, f))]
    dirs_name = [f for f in listdir(tests_abs_path) if not path.isfile(path.join(tests_abs_path, f))]
    for dir_name in dirs_name:
        curent_path = tests_abs_path + "/" + dir_name
        files_path = files_path + [path.join(curent_path, f) for f in listdir(curent_path) if
                                   path.isfile(path.join(curent_path, f))]
    return files_path
