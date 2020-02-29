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


def compare_images(image_b, base_screenshot_url, actual_screenshot_url, diff_screenshot_url, base_score):
    from skimage.measure import compare_ssim
    import imutils
    import cv2

    # load the two input images
    image_a = cv2.imread(base_screenshot_url)

    if image_a is None:
        os.makedirs(actual_screenshot_url[:actual_screenshot_url.rfind('/')], exist_ok=True)
        cv2.imwrite(actual_screenshot_url, image_b)
        raise AssertionError('There is no base image for: %s' % base_screenshot_url)

    # convert the images to grayscale
    gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    if gray_a.shape != gray_b.shape:
        os.makedirs(actual_screenshot_url[:actual_screenshot_url.rfind('/')], exist_ok=True)
        cv2.imwrite(actual_screenshot_url, image_b)
        raise AssertionError('Base: %s and\n Actual: %s\n have different sized' % (base_screenshot_url, actual_screenshot_url))

    (score, diff) = compare_ssim(gray_a, gray_b, full=True)
    if score < base_score:
        os.makedirs(actual_screenshot_url[:actual_screenshot_url.rfind('/')], exist_ok=True)
        os.makedirs(diff_screenshot_url[:diff_screenshot_url.rfind('/')], exist_ok=True)
        cv2.imwrite(actual_screenshot_url, image_b)
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


def get_horizontal_spacing(elem_1, elem_2):
    spacing = 0  # TODO

    return spacing


def get_vertical_spacing(elem_1, elem_2):
    spacing = 0  # TODO

    return spacing
