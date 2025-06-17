from django.core.cache.backends.base import BaseCache


class MockCacheTest(BaseCache):
    def __init__(self, location, params):
        super().__init__(params)

    def add(self, key, value, timeout=None, version=None):
        pass

    def get(self, key, default=None, version=None):
        return default

    def set(self, key, value, timeout=None, version=None):
        pass

    def delete(self, key, version=None):
        pass

    def clear(self):
        pass

    def delete_pattern(self, pattern, **options):
        pass

    def close(self, **kwargs):
        pass

    def incr(self, key, delta=1, version=None):
        pass

    def decr(self, key, delta=1, version=None):
        pass
