import os
import sys

import requests

from pytest_testrail.exceptions import MissingCloudCredentialError

# pylint: disable=import-error
if sys.version_info[0] == 2:
    import ConfigParser as configparser
else:
    import configparser


class Session:
    __default_headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'TestRail API v: 2'
    }

    def __init__(self, base_url: str = None, email: str = None, key: str = None, **kwargs):
        email = email or self.__get_credential('email', ['TESTRAIL_EMAIL'])
        key = key or self.__get_credential('key', ['TESTRAIL_KEY'])
        base_url = base_url or self.__get_credential('url', ['TESTRAIL_URL'])
        verify_ssl = bool(self.__get_credential('verify_ssl', ['TESTRAIL_VERIFY_URL']))

        self.__base_url = f'{base_url}/index.php?/api/v2/'
        self.__user = email
        self.__password = key
        self.__headers = kwargs.get('headers', self.__default_headers)
        self.__verify_ssl = kwargs.get('verify_ssl', verify_ssl)
        self.__timeout = kwargs.get('timeout', 5)
        self.__session = requests.Session()

    @property
    def __name(self):
        return type(self).__name__

    @property
    def __config(self):
        name = '.{0}'.format(self.__name.lower())
        config = configparser.ConfigParser()
        config.read([name, os.path.join(os.path.expanduser('~'), name)])
        return config

    def __get_credential(self, key, envs):
        try:
            return self.__config.get('credentials', key)
        except (configparser.NoSectionError, configparser.NoOptionError, KeyError):
            for env in envs:
                value = os.getenv(env)
                if value:
                    return value
        raise MissingCloudCredentialError(self.__name, key, envs)

    def request(self, method: str, src: str, **kwargs):
        """
        Base request method
        :param method:
        :param src:
        :param kwargs:
        :return: response
        """
        url = f'{self.__base_url}{src}'
        response = self.__session.request(method, url, auth=(self.__user, self.__password), headers=self.__headers,
                                          **kwargs)
        return response.json()
