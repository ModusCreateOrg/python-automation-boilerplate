from datetime import datetime, timedelta

from pytest_testrail.helper import custom_methods, TestRailError, testrail_duration_to_timedelta


class Result(object):
    def __init__(self, content=None):
        self._content = content or dict()
        self._custom_methods = custom_methods(self._content)

    def __getattr__(self, attr):
        if attr in self._custom_methods:
            return self._content.get(self._custom_methods[attr])
        raise AttributeError('"{}" object has no attribute "{}"'.format(
            self.__class__.__name__, attr))

    @property
    def assignedto_id(self):
        return self._content.get('assignedto_id')

    @assignedto_id.setter
    def assignedto_id(self, value):
        if not isinstance(value, int):
            raise TestRailError('input must be int')
        self._content['assignedto_id'] = value

    @property
    def comment(self):
        return self._content.get('comment')

    @comment.setter
    def comment(self, value):
        if not isinstance(value, str):
            raise TestRailError('input must be a string')
        self._content['comment'] = value

    @property
    def created_by(self):
        return self._content.get('created_by')

    @property
    def created_on(self):
        try:
            return datetime.fromtimestamp(int(self._content.get('created_on')))
        except TypeError:
            return None

    @property
    def defects(self):
        defects = self._content.get('defects')
        return defects.split(',') if defects else list()

    @defects.setter
    def defects(self, values):
        if not isinstance(values, list):
            raise TestRailError('input must be a list of strings')
        if not all(map(lambda x,: isinstance(x, str), values)):
            raise TestRailError('input must be a list of strings')
        if len(values) > 0:
            self._content['defects'] = ','.join(values)
        else:
            self._content['defects'] = None

    @property
    def elapsed(self):
        duration = self._content.get('elapsed')
        if duration is None:
            return None
        return testrail_duration_to_timedelta(duration)

    @elapsed.setter
    def elapsed(self, td):
        if not isinstance(td, timedelta):
            raise TestRailError('input must be a timedelta')
        if td > timedelta(weeks=10):
            raise TestRailError('maximum elapsed time is 10 weeks')
        self._content['elapsed'] = td.seconds

    @property
    def id(self):
        return self._content.get('id')

    @property
    def status_id(self):
        return self._content.get('status_id')

    @status_id.setter
    def status_id(self, value):
        if not isinstance(value, int):
            raise TestRailError('input must be int')
        self._content['status_id'] = value

    @property
    def test_id(self):
        return self._content.get('test_id')

    @test_id.setter
    def test_id(self, value):
        if not isinstance(value, int):
            raise TestRailError('input must be int')
        self._content['test_id'] = value

    @property
    def version(self):
        return self._content.get('version')

    @version.setter
    def version(self, ver):
        if not isinstance(ver, str):
            raise TestRailError('input must be a string')
        self._content['version'] = ver

    def raw_data(self):
        return self._content
