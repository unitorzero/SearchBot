import json
from json.decoder import JSONDecodeError


def loads(obj):
    if isinstance(obj, str):
        try:
            obj = json.loads(obj)
        except JSONDecodeError:
            return obj

    if isinstance(obj, list):
        obj = [loads(item) for item in obj]
        return obj

    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = loads(value)

    return obj


class RedisProperty:
    def __init__(self, redis, key, dump=False):
        self.redis = redis
        self.key = key
        self.dump = dump
        redis_value = self.redis.get(self.key)
        if redis_value:
            redis_value = redis_value.decode("utf-8")
        self._value = loads(redis_value) if dump and redis_value else redis_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        value = json.dumps(value) if self.dump else value
        self.redis.set(self.key, value)
