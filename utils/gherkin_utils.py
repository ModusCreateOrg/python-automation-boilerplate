from os import path, listdir

from gherkin.token_scanner import TokenScanner
from gherkin.parser import Parser


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
