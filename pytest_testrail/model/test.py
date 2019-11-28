from pytest_testrail.helper import custom_methods, testrail_duration_to_timedelta


class Test(object):
    def __init__(self, content=None):
        self._content = content or dict()
        self.custom_methods = custom_methods(self._content)

    def __getattr__(self, attr):
        if attr in self.custom_methods:
            return self._content.get(self._custom_methods[attr])
        raise AttributeError('"{}" object has no attribute "{}"'.format(
            self.__class__.__name__, attr))

    def __str__(self):
        return self.title

    @property
    def assignedto_id(self):
        return self._content.get('assignedto_id')

    @property
    def case_id(self):
        return self._content.get('case_id')

    @property
    def estimate(self):
        duration = self._content.get('estimate')
        if duration is None:
            return None
        return testrail_duration_to_timedelta(duration)

    @property
    def estimate_forecast(self):
        duration = self._content.get('estimate_forecast')
        if duration is None:
            return None
        return testrail_duration_to_timedelta(duration)

    @property
    def id(self):
        return self._content.get('id')

    @property
    def milestone_id(self):
        return self._content.get('milestone_id')

    @property
    def refs(self):
        return self._content.get('refs')

    @property
    def run_id(self):
        return self._content.get('run_id')

    @property
    def status_id(self):
        return self._content.get('status_id')

    @property
    def title(self):
        return self._content.get('title')

    def raw_data(self):
        return self._content
