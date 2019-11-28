import re
from datetime import timedelta


class TestRailError(Exception):
    pass


class ContainerIter:
    def __init__(self, objs):
        self._objs = list(objs)

    def __len__(self):
        return len(self._objs)

    def __getitem__(self, index):
        return self._objs[index]


CUSTOM_METHODS_RE = re.compile(r'^custom_(\w+)')


def custom_methods(content):
    matches = [CUSTOM_METHODS_RE.match(method) for method in content]
    return dict({match.string: content[match.string] for match in matches if match})


def testrail_duration_to_timedelta(duration):
    span = __span()
    timedelta_map = {
        'weeks': span(re.search(r'\d+w', duration)),
        'days': span(re.search(r'\d+d', duration)),
        'hours': span(re.search(r'\d+h', duration)),
        'minutes': span(re.search(r'\d+m', duration)),
        'seconds': span(re.search(r'\d+s', duration))
    }
    return timedelta(**timedelta_map)


def __span():
    return lambda x: int(x.group(0)[:-1]) if x else 0
