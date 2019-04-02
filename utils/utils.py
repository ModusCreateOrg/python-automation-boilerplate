import errno
import json
import os
from pathlib import Path
from os import path


def get_internationalization_values():
    raw_data = read_file('i18n.json')
    return raw_data


def get_users_values():
    raw_data = read_file('test_data/test_data.json')
    return raw_data['USERS']


def get_element_error_color_values():
    raw_data = read_file('test_data/test_data.json')
    return raw_data['ELEMENT_COLORS']


def get_password_masking_values():
    raw_data = read_file('test_data/test_data.json')
    return raw_data['PASSWORD_FIELD_TYPE']


def get_driver_params():
    raw_data = read_file('constants.json')
    return raw_data['driver']


def get_testrail_params():
    raw_data = read_file('constants.json')
    return raw_data['testrail_old']


def get_privacy_text_values():
    privacy_raw_data = read_file('test_data/text_content/eula_privacy_policy.txt')
    return privacy_raw_data


def get_terms_text_values():
    terms_raw_data = read_file('test_data/text_content/eula_terms_and_conditions_content.txt')
    return terms_raw_data


def read_file(file_name):
    # file_path = re.sub(r'utils.(\w+)', file_name, path.abspath(__file__))
    file_path = get_file_path(file_name)
    with open(file_path, encoding="utf-8") as fl:
        extension = path.splitext(file_path)[1]
        if extension == '.json':
            raw_data = json.load(fl)
            return raw_data
        elif extension == '.txt':
            raw_data = fl.read()
            return raw_data
        else:
            raise extension


def get_file_path(file_name):
    path_object = Path(file_name)
    if not path_object.exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_name)
    return path_object.resolve()
