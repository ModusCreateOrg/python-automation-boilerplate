from datetime import datetime

from pytest_testrail.helper import TestRailError


class Run(object):
    def __init__(self, content=None):
        self._content = content or dict()

    def __str__(self):
        return self.name

    @property
    def assignedto_id(self):
        return self._content.get('assignedto_id')

    @assignedto_id.setter
    def assignedto_id(self, value):
        if not isinstance(value, int):
            raise TestRailError('input must be int')
        self._content['assignedto_id'] = value

    @property
    def blocked_count(self):
        return self._content.get('blocked_count')

    @property
    def case_ids(self):
        return self._content.get('case_ids')

    @case_ids.setter
    def case_ids(self, value):
        self._content['case_ids'] = value

    @property
    def completed_on(self):
        try:
            return datetime.fromtimestamp(int(self._content.get('completed_on')))
        except TypeError:
            return None

    @property
    def config(self):
        return self._content.get('config')

    @property
    def config_ids(self):
        return self._content.get('config_ids')

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
    def custom_status_count(self):
        return self._content.get('custom_status_count')

    @property
    def description(self):
        return self._content.get('description')

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TestRailError('input must be string or None')
        self._content['description'] = value

    @property
    def failed_count(self):
        return self._content.get('failed_count')

    @property
    def id(self):
        return self._content.get('id')

    @property
    def include_all(self):
        return self._content.get('include_all')

    @include_all.setter
    def include_all(self, value):
        if not isinstance(value, bool):
            raise TestRailError('include_all must be a boolean')
        self._content['include_all'] = value

    @property
    def is_completed(self):
        return self._content.get('is_completed')

    @property
    def milestone(self):
        return self._content.get('milestone_id')

    @property
    def name(self):
        return self._content.get('name')

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TestRailError('input must be a string')
        self._content['name'] = value

    @property
    def passed_count(self):
        return self._content.get('passed_count')

    @property
    def plan_id(self):
        return self._content.get('plan_id')

    @property
    def project_id(self):
        return self._content.get('project_id')

    @property
    def retest_count(self):
        return self._content.get('retest_count')

    @property
    def suite_id(self):
        return self._content.get('suite_id')

    @suite_id.setter
    def suite_id(self, value):
        if not isinstance(value, int):
            raise TestRailError('input must be an int')
        self._content['suite_id'] = value

    @property
    def untested_count(self):
        return self._content.get('untested_count')

    @property
    def url(self):
        return self._content.get('url')

    def raw_data(self):
        return self._content
