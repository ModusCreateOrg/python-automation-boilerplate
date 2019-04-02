class Priority(object):
    def __init__(self, content):
        self._content = content

    def __str__(self):
        return self.name

    @property
    def id(self):
        return self._content.get('id')

    @property
    def is_default(self):
        return bool(self._content.get('is_default'))

    @property
    def level(self):
        return self._content.get('priority')

    @property
    def name(self):
        return self._content.get('name')

    @property
    def short_name(self):
        return self._content.get('short_name')
