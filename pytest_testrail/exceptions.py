import pytest


class MissingCloudCredentialError(pytest.UsageError):
    def __init__(self, driver, key, envs):
        super(MissingCloudCredentialError, self).__init__(
            "{0} {1} must be set. Try setting one of the following "
            "environment variables {2}, or see the documentation for "
            "how to use a configuration file.".format(driver, key, envs)
        )


class InvalidOptionError(Exception):
    def __init__(self, option):
        Exception.__init__(self, 'Option %s is not a valid choice' % option)
