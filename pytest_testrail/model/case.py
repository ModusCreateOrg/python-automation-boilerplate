from datetime import datetime

from pytest_testrail.helper import TestRailError, custom_methods


class Case(object):
    def __init__(self, content=None):
        self._content = content or dict()
        self._custom_methods = custom_methods(self._content)

    def __getattr__(self, attr):
        if attr in self._custom_methods:
            return self._content.get(self._custom_methods[attr])
        raise AttributeError('"{}" object has no attribute "{}"'.format(
            self.__class__.__name__, attr))

    def __str__(self):
        return self.title

    @property
    def created_by(self):
        return self._content.get('created_by')

    @property
    def created_on(self):
        return datetime.fromtimestamp(int(self._content.get('created_on')))

    @property
    def estimate(self):
        return self._content.get('estimate')

    @estimate.setter
    def estimate(self, value):
        # TODO should have some logic to validate format of timespan
        if not isinstance(value, str):
            raise TestRailError('input must be a string')
        self._content['estimate'] = value

    @property
    def estimated_forecast(self):
        return self._content.get('estimated_forecast')

    @property
    def id(self):
        return self._content.get('id')

    @property
    def milestone_id(self):
        return self._content.get('milestone_id')

    @milestone_id.setter
    def milestone_id(self, value):
        if not isinstance(value, int):
            raise TestRailError('input must be an int')
        self._content['milestone_id'] = value

    @property
    def priority_id(self):
        return self._content.get('priority_id')

    @priority_id.setter
    def priority_id(self, value):
        if not isinstance(value, int):
            raise TestRailError('input must be an int')
        self._content['priority_id'] = value

    @property
    def refs(self):
        refs = self._content.get('refs')
        return refs.split(',') if refs else list()

    @refs.setter
    def refs(self, value):
        if not isinstance(value, list):
            raise TestRailError('input must be a list')
        self._content['refs'] = ','.join(value)

    @property
    def section_id(self):
        return self._content.get('section_id')

    @section_id.setter
    def section_id(self, value):
        if not isinstance(value, int):
            raise TestRailError('input must be an int')
        self._content['section_id'] = value

    @property
    def suite_id(self):
        return self._content.get('suite_id')

    @suite_id.setter
    def suite_id(self, value):
        if not isinstance(value, int):
            raise TestRailError('input must be an int')
        self._content['suite_id'] = value

    @property
    def template_id(self):
        return self._content.get('template_id')

    @template_id.setter
    def template_id(self, value):
        if not isinstance(value, int):
            raise TestRailError('input must be an id')
        self._content['template_id'] = value

    @property
    def title(self):
        return self._content.get('title')

    @title.setter
    def title(self, value):
        if not isinstance(value, (str, str)):
            raise TestRailError('input must be a string')
        self._content['title'] = value

    @property
    def type_id(self):
        return self._content.get('type_id')

    @type_id.setter
    def type_id(self, value):
        if not isinstance(value, int):
            raise TestRailError('input must be an id')
        self._content['type_id'] = value

    @property
    def updated_by(self):
        return self._content.get('updated_by')

    @property
    def updated_on(self):
        return datetime.fromtimestamp(int(self._content.get('updated_on')))

    def raw_data(self):
        return self._content
