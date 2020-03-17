import os
from threading import Lock


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """
    _instance = None

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    def __call__(cls, *args, **kwargs):
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if not cls._instance:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class EnvVariables(metaclass=SingletonMeta):
    def __init__(self, env_vars_file_path) -> None:
        from dotenv import load_dotenv
        load_dotenv(dotenv_path=env_vars_file_path, verbose=True)
        self.env = env_vars_file_path

    @property
    def base_url(self):
        return os.getenv("BASE_URL")

    @property
    def login_url(self):
        return os.getenv("LOGIN_URL")

    @property
    def basic_auth_username(self):
        return os.getenv("BASIC_AUTH_USERNAME")

    @property
    def basic_auth_password(self):
        return os.getenv("BASIC_AUTH_PASSWORD")

    @property
    def login_username(self):
        return os.getenv("LOGIN_USERNAME")

    @property
    def login_password(self):
        return os.getenv("LOGIN_PASSWORD")

    @property
    def content_editor_username(self):
        return os.getenv("CONTENT_EDITOR_USERNAME")

    @property
    def content_editor_password(self):
        return os.getenv("CONTENT_EDITOR_PASSWORD")
