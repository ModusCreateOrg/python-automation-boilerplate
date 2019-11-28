from datetime import datetime

from pytest_testrail.helper import TestRailError
from pytest_testrail.model.run import Run


class Plan(object):
    def __init__(self, content=None):
        self._content = content or dict()

    def __str__(self):
        return self.name

    @property
    def assignedto_id(self):
        return self._content.get('assignedto_id')

    @property
    def blocked_count(self):
        return self._content.get('blocked_count')

    @property
    def completed_on(self):
        try:
            return datetime.fromtimestamp(int(self._content.get('completed_on')))
        except TypeError:
            return None

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
            raise TestRailError('input must be a string')
        self._content['description'] = value

    @property
    def entries(self):
        return list(map(Entry, self._content.get('entries')))

    @property
    def failed_count(self):
        return self._content.get('failed_count')

    @property
    def id(self):
        return self._content.get('id')

    @property
    def is_completed(self):
        return self._content.get('is_completed')

    @property
    def milestone_id(self):
        return self._content.get('milestone_id')

    @milestone_id.setter
    def milestone_id(self, value):
        if not isinstance(value, int):
            raise TestRailError('input must be an int')
        self._content['milestone_id'] = value

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
    def project_id(self):
        return self._content.get('project_id')

    @property
    def retest_count(self):
        return self._content.get('retest_count')

    @property
    def untested_count(self):
        return self._content.get('untested_count')

    @property
    def url(self):
        return self._content.get('url')

    def raw_data(self):
        return self._content


class Entry(object):
    def __init__(self, content):
        self._content = content

    @property
    def assigned_to(self):
        return self._content.get('assignedto_id')

    @property
    def case_ids(self):
        return self._content.get('case_ids')

    @case_ids.setter
    def case_ids(self, value):
        self._content['case_ids'] = value

    @property
    def description(self):
        return self._content.get('description')

    @description.setter
    def description(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise TestRailError('input must be string or None')
        self._content['description'] = value

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
    def name(self):
        return self._content.get('name')

    @property
    def runs(self):
        return list(map(RunEntry, self._content.get('runs')))

    @runs.setter
    def runs(self, value):
        self._content['runs'] = value

    @property
    def suite_id(self):
        return self._content.get('suite_id')

    @suite_id.setter
    def suite_id(self, value):
        if not isinstance(value, str):
            raise TestRailError('input must be an int')
        self._content['suite_id'] = value

    def raw_data(self):
        return self._content


class RunEntry(Run):
    def __init__(self, content):
        super(RunEntry, self).__init__(content)

    @property
    def entry_id(self):
        return self._content.get('entry_id')

    @property
    def entry_index(self):
        return self._content.get('entry_index')
