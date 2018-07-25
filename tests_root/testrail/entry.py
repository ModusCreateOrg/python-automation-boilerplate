from testrail.base import TestRailBase
from testrail.api import API
from testrail.run import Run
from testrail.suite import Suite
from testrail.case import Case
from testrail.user import User
from testrail.helper import TestRailError


class EntryRun(Run):
    def __init__(self, content):
        super(EntryRun, self).__init__(content)

    @property
    def entry_id(self):
        return self._content.get('entry_id')

    @property
    def entry_index(self):
        return self._content.get('entry_index')


class Entry(TestRailBase):
    def __init__(self, content):
        self._content = content
        self._api = API()

    @property
    def id(self):
        return self._content.get('id')

    @property
    def name(self):
        return self._content.get('name')

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
    def assigned_to(self):
        return User(self._api.user_with_id(self._content.get('assignedto_id')))

    @property
    def suite(self):
        return Suite(self._api.suite_with_id(self._content.get('suite_id')))

    @property
    def include_all(self):
        return self._content.get('include_all')

    @include_all.setter
    def include_all(self, value):
        if not isinstance(value, bool):
            raise TestRailError('include_all must be a boolean')
        self._content['include_all'] = value

    @property
    def cases(self):
        if self._content.get('case_ids'):
            cases = list(map(self.api.case_with_id, self._content.get('case_ids')))
            return list(map(Case, cases))
        else:
            return list()

    @cases.setter
    def cases(self, cases):
        exc_msg = 'cases must be set to None or a container of Case objects'

        if cases is None:
            self._content['case_ids'] = None

        elif not isinstance(cases, (list, tuple)):
            raise TestRailError(exc_msg)

        elif not all([isinstance(case, Case) for case in cases]):
            raise TestRailError(exc_msg)

        else:
            self._content['case_ids'] = [case.id for case in cases]

    @property
    def runs(self):
        return map(EntryRun, self._content.get('runs'))

    def raw_data(self):
        return self._content
