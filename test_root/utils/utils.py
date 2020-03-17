# pylint: disable=import-outside-toplevel
# pylint: disable=no-member
import errno
import json
import os
from os import path, strerror
from pathlib import Path

import pytest


def get_env_name(caps: dict):
    os = caps['os'] if 'os' in caps else None
    os_version = caps['os_version'] if 'os_version' in caps else ''
    env = caps['browser'] if 'browser' in caps else caps['device'] if 'device' in caps else ''

    if os is None:
        return '%s - %s' % (env, os_version)
    return '%s %s - %s' % (os, os_version, env)


def initialize_screenshot_dirs():
    import os
    project_pwd = os.path.dirname(__file__)
    pytest.globalDict['base_screenshot_dir'] = project_pwd.replace('/utils', '') + '/screenshots/base'
    pytest.globalDict['actual_screenshot_dir'] = project_pwd.replace('/utils', '') + '/screenshots/actual'
    pytest.globalDict['diff_screenshot_dir'] = project_pwd.replace('/utils', '') + '/screenshots/diff'


def read_file(file_name):
    # file_path = re.sub(r'utils.(\w+)', file_name, path.abspath(__file__))
    file_path = get_file_path(file_name)
    with open(file_path, encoding="utf-8") as fl:
        extension = path.splitext(file_path)[1]
        if extension == '.json':
            raw_data = json.load(fl)
            return raw_data
        if extension == '.txt':
            raw_data = fl.read()
            return raw_data
        raise extension


def get_file_path(file_name):
    path_object = Path(file_name)
    if not path_object.exists():
        raise FileNotFoundError(errno.ENOENT, strerror(errno.ENOENT), file_name)
    return path_object.resolve()
