import logging
from BotStepper.utils.RedisProperty import RedisProperty


class UserState:
    log = logging

    def __init__(self, redis, telegram_id):
        self.telegram_id = telegram_id
        self.redisProperty = RedisProperty(redis, self.generate_redis_state_key(self.telegram_id), dump=True)
        self._step = self.redisProperty.value.get('step') if self.redisProperty.value else None
        self.params = self.redisProperty.value.get('params') or {} if self.redisProperty.value else {}

    @property
    def step(self):
        return self._step

    def set_step(self, value):
        self._step = value
        self.log.info('Set step %s' % value)
        return self

    def get_parameter(self, key):
        return self.params.get(key) or {}

    def set_parameter(self, key, value):
        self.params[key] = value
        return self

    def save(self):
        self.redisProperty.value = {
            'step': self._step,
            'params': self.params
        }
        return self

    @staticmethod
    def generate_redis_state_key(user_id):
        return 'state_user:{}'.format(user_id)
