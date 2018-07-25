from collections import defaultdict
from os import listdir, path
import pytest
from tests.testrail_integration.file_parser import get_feature
from tests.testrail_integration.testrail_utils import initialize_testrail_client, \
    setup_test_plan, publish_tests, get_test_from_scenario, publish_tests_results
from tests.utils import get_project_params, get_internationalization_values, get_testrail_params

# pylint: disable=invalid-name
pytest_plugins = [
    "tests.test_assertions",
    "tests.test_common"
]


def pytest_configure():
    pytest.globalDict = defaultdict()


def pytest_addoption(parser):
    parser.addoption("--publish",
                     action="store",
                     default=False,
                     type=bool,
                     help="If true will publish tests to TestRail")
    parser.addoption("--object_path",
                     action="store",
                     default=None,
                     type=str,
                     help=".feature file to publish tests from")
    parser.addoption("--not_publish_results",
                     action="store",
                     default=False,
                     type=bool,
                     help="If true will not publish test results to TestRail")


def pytest_collection_modifyitems(items, config):
    publish = config.option.publish

    if publish is True:
        # Un-select all tests. Publishing is selected
        config.hook.pytest_deselected(items=[])
        items[:] = []

        object_path = config.option.object_path
        project_id = pytest.globalDict['project']['id']
        project_name = pytest.globalDict['project']['name']
        tr = initialize_testrail_client(project_id)

        if path.isfile(object_path):
            feature = get_feature(object_path)
            publish_tests(tr, project_name, feature)
        else:
            files_name = [f for f in listdir(object_path) if path.isfile(path.join(object_path, f))]
            for file_name in files_name:
                feature = get_feature(path.join(object_path, file_name))
                publish_tests(tr, project_name, feature)


def pytest_bdd_apply_tag(function):
    scenario_tags = function.func_globals['feature'].tags.union(function.func_globals['scenario'].tags)
    if not 'automated' in scenario_tags:
        marker = pytest.mark.skip(reason="Not implemented yet")
        marker(function)
        return True

    market_tags = filter(lambda scenario_tag: scenario_tag.startswith('market_'), scenario_tags)
    not_market_tags = filter(lambda scenario_tag: scenario_tag.startswith('not_market_'), scenario_tags)
    if (market_tags.__len__() != 0 and 'market_en' not in market_tags) or \
       (not_market_tags.__len__() != 0 and 'not_market_en' in not_market_tags):
        marker = pytest.mark.skip(reason="Not in scope of current market")
        marker(function)
        return True

    test_scope = pytest.globalDict['project']['suites']
    if test_scope.__len__() != 0 \
            and not any(suite in function.func_globals['feature_name'] for suite in test_scope):
        marker = pytest.mark.skip(reason="Not in scope of testing. See: PROJECT_DICT.suites")
        marker(function)
        return True

    # Fall back to pytest-bdd's default behavior
    return None


@pytest.fixture
def pytest_bdd_before_scenario():
    pass


@pytest.fixture
def pytest_bdd_after_scenario(request, feature, scenario):

    # Adding Scenario to the list of Scenarios ran
    if 'scenarios' in pytest.globalDict:
        scenarios = pytest.globalDict['scenarios']

        tr = pytest.globalDict['tr']
        tr_test_plan = pytest.globalDict['tr_test_plan']
        test_env = pytest.globalDict['project']['env']
        tr_run_test = get_test_from_scenario(tr, tr_test_plan, test_env, request, feature, scenario)
        if isinstance(tr_run_test, basestring):
            pytest.raises(ValueError, message=tr_run_test)

        if feature.name in scenarios:
            scenarios[feature.name].append(tr_run_test)
        else:
            scenarios.update({feature.name: []})
            scenarios[feature.name].append(tr_run_test)

        pytest.globalDict['scenarios'] = scenarios


@pytest.fixture
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


@pytest.fixture
def pytestbdd_strict_gherkin():
    return False


def pytest_sessionstart(session):
    pytest.globalDict['project'] = get_project_params()
    pytest.globalDict['i18n'] = get_internationalization_values()[pytest.globalDict['project']['language']]

    testrail_params = get_testrail_params()
    not_publish_results = session.config.option.not_publish_results or testrail_params['not_publish_results']
    if not not_publish_results:
        project_id = pytest.globalDict['project']['id']
        project_name = pytest.globalDict['project']['name']
        test_plan = pytest.globalDict['project']['test_plan']
        test_env = pytest.globalDict['project']['env']
        test_scope = pytest.globalDict['project']['suites']
        test_market = pytest.globalDict['project']['market']
        tr = initialize_testrail_client(project_id)
        tr_test_plan = setup_test_plan(tr, project_name, test_plan, test_env, test_market, test_scope)

        pytest.globalDict['tr'] = tr
        pytest.globalDict['tr_test_plan'] = tr_test_plan
        pytest.globalDict['scenarios'] = {}


def pytest_sessionfinish(session):
    testrail_params = get_testrail_params()
    not_publish_results = session.config.option.not_publish_results or testrail_params['not_publish_results']
    if not not_publish_results:
        tr = pytest.globalDict['tr']
        tr_test_plan = pytest.globalDict['tr_test_plan']
        test_run = pytest.globalDict['scenarios']
        test_env = pytest.globalDict['project']['env']

        publish_tests_results(tr, tr_test_plan, test_run, test_env)
