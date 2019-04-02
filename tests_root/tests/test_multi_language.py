import pytest
from pytest_bdd import when, parsers
from pytest_bdd import scenarios


scenarios('features/multi_language.feature')


@when(parsers.re('I have text <(?P<key>(.*)+)>'), converters=dict(key=str))
def i_have_text(key):
    if 'texts' not in pytest.globalDict.keys():
        pytest.globalDict['texts'] = []
    pytest.globalDict['texts'].append(pytest.globalDict['i18n'][key])


@when('I merge the texts')
def merge_texts():
    pytest.globalDict['text'] = ' '.join(pytest.globalDict['texts'])
