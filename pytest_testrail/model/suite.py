from datetime import datetime

from pytest_testrail.helper import TestRailError


class Suite(object):
    def __init__(self, content=None):
        self._content = content or dict()

    def __str__(self):
        return self.name

    @property
    def completed_on(self):
        try:
            return datetime.fromtimestamp(int(self._content.get('completed_on')))
        except TypeError:
            return None

    @property
    def description(self):
        return self._content.get('description')

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TestRailError('input must be a string')
        self._content['description'] = value

    @property
    def id(self):
        return self._content.get('id')

    @property
    def is_baseline(self):
        return self._content.get('is_baseline')

    @property
    def is_completed(self):
        return self._content.get('is_completed')

    @property
    def is_master(self):
        return self._content.get('is_master')

    @property
    def name(self):
        return self._content.get('name')

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TestRailError('input must be a string')
        self._content['name'] = value

    @property
    def project_id(self):
        return self._content.get('project_id')

    @project_id.setter
    def project_id(self, value):
        if not isinstance(value, int):
            raise TestRailError('input must be an int')
        self._content['project_id'] = value

    @property
    def url(self):
        return self._content.get('url')

    def raw_data(self):
        return self._content
