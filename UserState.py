from BotStepper.utils.UserState import UserState
from config import DEFAULT_LOCALE
from db.bot_orm.tables.requests import Requests
from bot_redis.storeges import users
import logging


class UserStateInfo(UserState):
    log = logging

    def __init__(self, redis, telegram_id):
        super().__init__(redis, telegram_id)
        self.permissions = []
        self.inline_msg = self.params.get('inline_msg', {})
        self.locale = self.params.get('locale', DEFAULT_LOCALE)
        self.user = users.get_user_by_telegram_id(self.telegram_id)
        self._step_params = self.params.get('step_params', {})

    def set_permissions(self, permissions):
        self.permissions = permissions

    def log_request(self, filters):
        Requests.add(self.user.id, filters)
        return self

    def get_filters(self):
        return self.params.get('filters') or {}

    def set_filters(self, filters):
        self.params['filters'] = filters
        return self

    def _generate_filter_obj(self, type_value, value):
        return {'value': value, 'type': type_value}

    def set_filter(self, key, type_value, value):
        filters = self.get_filters()
        filters[key] = self._generate_filter_obj(type_value, value)
        self.set_filters(filters)
        self.log.info('set %s[%s] filter: %s' % (key, type_value, value))
        return self

    def delete_filter(self, key):
        filters = self.get_filters()
        filters.pop(key)
        self.set_filters(filters)
        self.log.info('delete filter %s' % key)
        return self

    def clear_filters(self):
        self.set_filters({})
        self.log.info('Filters was cleared.')
        return self

    def get_inline_msg(self, msg_id):
        return self.inline_msg.get(str(msg_id), {})

    def get_inline_msg_all(self):
        return self.inline_msg

    def update_inline_msg(self):
        self.params['inline_msg'] = self.inline_msg
        return self

    def del_inline_msg(self, msg_id):
        self.log.info('Cleared inline msg %s' % self.inline_msg.get(str(msg_id)))
        self.inline_msg.pop(str(msg_id))
        return self

    def set_inline_msg(self, msg_id, params):
        self.inline_msg[str(msg_id)] = params
        self.log.info('New/update inline msg %s' % params)
        return self.update_inline_msg()

    @property
    def step_params(self):
        return self._step_params

    @step_params.setter
    def step_params(self, value):
        self._step_params = value
        self.params['step_params'] = self._step_params
        self.save()
