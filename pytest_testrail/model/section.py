from pytest_testrail.helper import TestRailError


class Section(object):
    def __init__(self, content=None):
        self._content = content or dict()

    def __str__(self):
        return self.name

    @property
    def depth(self):
        return self._content.get('depth')

    @property
    def description(self):
        return self._content.get('description')

    @property
    def display_order(self):
        return self._content.get('display_order')

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TestRailError('input must be a string')
        self._content['description'] = value

    @property
    def id(self):
        return self._content.get('id')

    @property
    def name(self):
        return self._content.get('name')

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TestRailError('input must be a string')
        self._content['name'] = value

    @property
    def suite_id(self):
        return self._content.get('suite_id')

    @suite_id.setter
    def suite_id(self, value):
        if not isinstance(value, int):
            raise TestRailError('input must be an int')
        self._content['suite_id'] = value

    @property
    def parent_id(self):
        return self._content.get('parent_id')

    @parent_id.setter
    def parent_id(self, value):
        if not isinstance(value, int):
            raise TestRailError('input must be an int')
        self._content['parent_id'] = value

    def raw_data(self):
        return self._content
