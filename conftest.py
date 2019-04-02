# pylint: disable=invalid-name
from collections import defaultdict
from copy import copy

import pytest

from testrail.testrail_api import TestRailAPI
from testrail.testrail_utils import export_tests, export_tests_results
from utils.gherkin_utils import get_feature, get_feature_files_path
from webdriver import custom_driver
from webdriver.custom_webdriver import WebDriverCustom

pytest_plugins = [
    'pytest_selenium',
    'tests/test_assertions',
    'tests/test_common'
]


def pytest_configure(config):
    config.option.keyword = 'automated'
    config.option.markexpr = 'not not_in_scope'
    pytest.globalDict = defaultdict()
    pass


@pytest.fixture(scope='session')
def language(request):
    config = request.config
    language = config.getoption('language')
    if language is not None:
        return language


def pytest_addoption(parser):
    parser.addoption('--language',
                     action='store',
                     default='en',
                     type=str,
                     help='Application language')
    parser.addoption('--export_tests_path',
                     metavar="str",
                     help='Will export tests form given file or directory to TestRail')
    parser.addoption('--export_results',
                     action='store_true',
                     help='If false will not publish results to TestRail')
    parser.addoption('--tags',
                     metavar="str",
                     help='Will filter tests by given tags')


def pytest_collection_modifyitems(config, items):
    export_tests_path = config.option.export_tests_path
    if export_tests_path:
        print('\nUn-select all tests. Exporting is selected')
        for item in items:
            item.add_marker(pytest.mark.not_in_scope)

    raw_tags = config.option.tags
    if raw_tags:
        print('\nFilter tests by given tags: %s' % raw_tags)
        tags = raw_tags.split(',')
        filter_collection_by_tags(items, tags)


def filter_collection_by_tags(items, tags):
    for item in items:
        has_tag = False
        for tag in tags:
            if tag.startswith('not:'):
                if any(m.name == tag.replace('not:', '') for m in item.own_markers):
                    item.add_marker(pytest.mark.not_in_scope)
            else:
                if any(m.name == tag for m in item.own_markers):
                    has_tag = True
        if not has_tag:
            item.add_marker(pytest.mark.not_in_scope)


def pytest_sessionstart(session):
    pytest.globalDict['implicit_wait_time'] = session.config._variables['driver']['implicit_wait_time']

    export_tests_path = session.config.option.export_tests_path
    export_results = session.config.option.export_results
    if export_results is True and bool(export_tests_path) is True:
        raise ValueError('Cannot export "Test Cases" and "Test Results" at the same time')
    pass

    project_variables = session.config._variables['project']
    pytest.globalDict['project'] = project_variables
    pytest.globalDict['scenarios_run'] = []

    env_name = get_env_name(session.config.option.driver, session.config._capabilities)
    pytest.globalDict['env_name'] = env_name


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
        os_name = caps['deviceName']
        os_version = '_%s' % caps['platformVersion']
        browser_name = '-app'
        pass
    else:
        import platform
        os_name = 'macOS' if platform.platform().__contains__('Darwin') else 'Windows'
        os_version = '_Mojave' if platform.platform().__contains__('Darwin') else '_10'
        browser_name = '-%s' % driver_name
    return '%s%s%s' % (os_name, os_version, browser_name)


def pytest_sessionfinish(session):
    export_tests_path = session.config.option.export_tests_path
    export_results = session.config.option.export_results

    project_variables = session.config._variables['project']

    if export_tests_path:
        print('Initialize TestRail client')
        tr = TestRailAPI()
        export_feature_files(tr, project_variables, export_tests_path)

    if export_results:
        print('Initialize TestRail client')
        scenarios_run = pytest.globalDict['scenarios_run']
        env_name = pytest.globalDict['env_name']
        tr = TestRailAPI()
        export_tests_results(tr, project_variables, scenarios_run, env_name)


def export_feature_files(tr: TestRailAPI, project_variables: dict, export_tests_path: str):
    files_path = get_feature_files_path(export_tests_path)
    for file_path in files_path:
        feature = get_feature(file_path)
        export_tests(tr, project_variables['id'], feature)


def pytest_bdd_after_scenario(request, feature, scenario):
    # Adding Scenario to the list of Scenarios ran
    scenario.data_set = {}
    for key, value in request.node.funcargs.items():
        if key in scenario.params:
            scenario.data_set.update({key: value})
    pytest.globalDict['scenarios_run'].append(copy(scenario))


def pytest_bdd_step_error(scenario, step, exception):
    scenario.exception = exception
    scenario.failed = True

    # Setting Scenario and Steps statuses and exception error if the case
    flag = False
    for scenario_step in scenario.steps:
        scenario_step.failed = None if flag else False
        if scenario_step == step:
            scenario_step.exception = exception
            scenario_step.failed = True
            flag = True
    print('Following step FAILED: %s' % step.name)
    exception_message = exception.msg if hasattr(exception, 'msg') \
        else exception.message if hasattr(exception, 'message') \
        else exception.args[0] if hasattr(exception, 'args') \
        else 'no error message'
    scenario.exception_message = exception_message
    print('Error: %s' % exception_message)


@pytest.fixture(scope="session")
def driver_class(request, driver_class):
    driver = request.config.getoption("driver")
    if driver == 'Custom_Driver':
        request.config.pluginmanager.getplugin('pytest_selenium') \
            .drivers.__dict__.update({'custom_driver': custom_driver})
        return WebDriverCustom
    return driver_class
