from collections import defaultdict
import pytest
from tests.conf_driver import set_up, tear_down
from tests.utils import get_project_params, get_internationalization_values

pytest_plugins = [
    "tests.test_common"
]



def pytest_configure():
    pytest.globalDict = defaultdict()


def pytest_addoption(parser):
    pass


def pytest_collection_modifyitems(items, config):
    pass


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
    set_up()


@pytest.fixture
def pytest_bdd_after_scenario(request, feature, scenario):
    tear_down()


@pytest.fixture
def pytestbdd_strict_gherkin():
    return False


def pytest_sessionstart(session):
    pytest.globalDict['project'] = get_project_params()
    pytest.globalDict['i18n'] = get_internationalization_values()[pytest.globalDict['project']['language']]
    pytest.globalDict['scenarios'] = {}


def pytest_sessionfinish():
    pass


@pytest.fixture
def driver():
    return pytest.globalDict['driver']
