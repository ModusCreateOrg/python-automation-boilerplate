# pylint: disable=invalid-name
# pylint: disable=protected-access
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

from collections import defaultdict
from copy import deepcopy

import pytest
from pytest_testrail.testrail_api import TestRailAPI
from pytest_testrail.testrail_utils import export_tests, export_tests_results

from tests.test_context import *
from tests.test_actions import *
from tests.test_assertions import *
from utils.gherkin_utils import get_feature_files_path, get_feature
from utils.utils import initialize_screenshot_dirs, get_env_name
from webdriver.custom_commands import add_custom_commands

pytest_plugins = [
    'pytest_testrail',
]


def pytest_configure(config):
    config.option.keyword = 'automated'
    config.option.markexpr = 'not not_in_scope'
    pytest.globalDict = defaultdict()


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
                    has_tag = True
            else:
                if any(m.name == tag for m in item.own_markers):
                    has_tag = True
        if not has_tag:
            item.add_marker(pytest.mark.not_in_scope)


def pytest_sessionstart(session):
    pytest.globalDict['env'] = session.config._variables['env'] if 'env' in session.config._variables else {}

    export_tests_path = session.config.option.export_tests_path
    export_results = session.config.option.export_results
    if export_results is True and bool(export_tests_path) is True:
        raise ValueError('Cannot export "Test Cases" and "Test Results" at the same time')

    project_variables = session.config._variables['project']
    pytest.globalDict['project'] = project_variables
    pytest.globalDict['scenarios_run'] = {}

    pytest.globalDict['i18n'] = session.config._variables[project_variables['language']]

    env_name = get_env_name(session.config._capabilities)
    pytest.globalDict['env_name'] = env_name

    headless_chrome = session.config._capabilities['headless'] in ['true', 'True', '1', 'ty', 'Y'] \
        if 'headless' in session.config._capabilities else False
    pytest.globalDict['headless_chrome'] = headless_chrome

    initialize_screenshot_dirs()
    add_custom_commands()


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


def pytest_bdd_after_scenario(request, feature, scenario):
    # Adding Scenario to the list of Scenarios ran
    if request.config.option.export_results:
        add_scenario_to_run(request, scenario)
    if request.config.option.reruns >= request.node.execution_count:
        scenario.failed = False
        for scenario_step in scenario.steps:
            scenario_step.failed = False


def pytest_bdd_step_error(request, scenario, step, exception):
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


def export_feature_files(tr: TestRailAPI, project_variables: dict, export_tests_path: str):
    files_path = get_feature_files_path(export_tests_path)
    for file_path in files_path:
        feature = get_feature(file_path)
        export_tests(tr, project_variables['id'], project_variables['name'], feature)


def add_scenario_to_run(request, scenario):
    scenario.data_set = {}
    for key, value in request.node.funcargs.items():
        if key in scenario.params:
            scenario.data_set.update({key: value})

    suite_name = scenario.feature.name.split(' - ')[0]
    if suite_name not in pytest.globalDict['scenarios_run']:
        pytest.globalDict['scenarios_run'][suite_name] = []
    pytest.globalDict['scenarios_run'][suite_name].append(deepcopy(scenario))


@pytest.fixture
def selenium(selenium):
    selenium.set_page_load_timeout(90)
    selenium.implicitly_wait(60)
    selenium.set_script_timeout(60)
    return selenium


@pytest.fixture
def chrome_options(chrome_options):
    if pytest.globalDict['headless_chrome'] is True:
        chrome_options.add_argument('--headless')
    return chrome_options


@pytest.fixture
def capabilities(capabilities):
    if capabilities['browser'] in ['Edge', 'MicrosoftEdge']:
        capabilities['browserstack.edge.enablePopups'] = 'true'
    if capabilities['browser'] in ['safari', 'Safari']:
        capabilities['browserstack.safari.enablePopups'] = 'true'
    return capabilities


@pytest.fixture(scope='session')
def language(request):
    config = request.config
    language = config.getoption('language')
    if language is not None:
        return language
    return None
