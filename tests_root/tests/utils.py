import json
import re
from os import path, environ


def get_project_params():
    raw_data = read_file('constants.json')
    project_data = {
        'suites': raw_data['project']['suites'],
        'tags': environ.get('test_tags') or raw_data['project']['tags'],
        'language': environ.get('project_language') or raw_data['project']['language'],
        'market': environ.get('project_market') or raw_data['project']['market']
    }
    return project_data


def get_internationalization_values():
    raw_data = read_file('i18n.json')
    return raw_data


def get_driver_params():
    raw_data = read_file('constants.json')
    return raw_data['driver']


def read_file(file_name):
    file_path = re.sub(r'utils.(\w+)', file_name, path.abspath(__file__))
    with open(file_path) as fl:
        raw_data = json.load(fl)
        return raw_data
