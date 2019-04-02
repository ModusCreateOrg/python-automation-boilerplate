import pytest
from pytest_bdd import then, parsers


@then(parsers.parse('The result should be {result:d} on the screen'))
@then(parsers.parse('The result should be <result> on the screen'))
def result_of_arithmetic(result):
    assert pytest.globalDict['sum'] == result


@then(parsers.re('I get text <(?P<key_1>(.*)+)> <(?P<key_2>(.*)+)> <(?P<key_3>(.*)+)>'),
      converters=dict(key_1=str, key_2=str, key_3=str))
def text_validation(key_1, key_2, key_3):
    assert pytest.globalDict['text'] == \
           pytest.globalDict['i18n'][key_1] + ' ' + \
           pytest.globalDict['i18n'][key_2] + ' ' + \
           pytest.globalDict['i18n'][key_3]
