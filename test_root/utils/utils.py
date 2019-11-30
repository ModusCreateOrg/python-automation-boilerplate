# pylint: disable=import-outside-toplevel
# pylint: disable=no-member
import errno
import json
from pathlib import Path
from os import path, strerror

import pytest


def get_env_name(driver_name: str, caps: dict):
    if driver_name == 'BrowserStack':
        os_name = caps['os'] if 'os' in caps else caps['device']
        os_version = '_%s' % caps['os_version']
        browser_name = '-%s' % caps['browser'] if 'browser' in caps else '-web'
    elif driver_name == 'BrowserStack_app':
        os_name = caps['device']
        os_version = '_%s' % caps['os_version']
        browser_name = '-app'
    elif driver_name in ['Appium', 'Custom_Driver']:
        os_name = caps['deviceName'] if 'deviceName' in caps else caps['device'] \
            if 'device' in caps else caps['os']
        os_version = '_%s' % caps['platformVersion'] if 'platformVersion' in caps else caps['os_version'] \
            if 'os_version' in caps else caps['browser_version']
        browser_name = '-app' if 'deviceName' in caps else caps['browser'] \
            if 'browser' in caps else '-native-browser'
    else:
        import platform
        os_name = 'macOS' if platform.platform().__contains__('Darwin') else 'Windows'
        os_version = '_Mojave' if platform.platform().__contains__('Darwin') else '_10'
        browser_name = '-%s' % driver_name
    return '%s%s%s' % (os_name, os_version, browser_name)


def initialize_screenshot_dirs():
    import os
    project_pwd = os.path.dirname(__file__)
    pytest.globalDict['base_screenshot_dir'] = project_pwd.replace('/utils', '') + '/screenshots'
    pytest.globalDict['actual_screenshot_dir'] = project_pwd.replace('/utils', '') + '/screenshots'
    pytest.globalDict['diff_screenshot_dir'] = project_pwd.replace('/utils', '') + '/screenshots'
    if not os.path.exists(pytest.globalDict['actual_screenshot_dir']):
        os.makedirs(pytest.globalDict['actual_screenshot_dir'])
    if not os.path.exists(pytest.globalDict['diff_screenshot_dir']):
        os.makedirs(pytest.globalDict['diff_screenshot_dir'])


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
        if extension == '.txt':
            raw_data = fl.read()
            return raw_data
        raise extension


def get_file_path(file_name):
    path_object = Path(file_name)
    if not path_object.exists():
        raise FileNotFoundError(errno.ENOENT, strerror(errno.ENOENT), file_name)
    return path_object.resolve()


def compare_images(base_screenshot_url, actual_screenshot_url, diff_screenshot_url):
    from skimage.measure import compare_ssim
    import imutils
    import cv2

    # load the two input images
    image_a = cv2.imread(base_screenshot_url)
    image_b = cv2.imread(actual_screenshot_url)
    cv2.imwrite(actual_screenshot_url, image_b)

    # convert the images to grayscale
    gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(gray_a, gray_b, full=True)

    if score != 1.0:
        diff = (diff * 255).astype("uint8")

        # threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for cnt in cnts:
            # compute the bounding box of the contour and then draw the
            # bounding box on both input images to represent where the two
            # images differ
            (x_point, y_point, width, height) = cv2.boundingRect(cnt)
            cv2.rectangle(image_b, (x_point, y_point), (x_point + width, y_point + height), (0, 0, 255), 2)

        cv2.imwrite(diff_screenshot_url, image_b)

    return score
