class CaseType(object):
    def __init__(self, content):
        self._content = content

    def __str__(self):
        return self.name

    @property
    def id(self):
        return self._content.get('id')

    @property
    def is_default(self):
        return self._content.get('is_default')

    @property
    def name(self):
        return self._content.get('name')
