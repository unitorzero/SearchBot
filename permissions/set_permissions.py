from bot_redis.storeges import users
from keys import PERMISSIONS
from BotStepper.utils.utils import get_chat_id


def add_permissions_by_user_id(user_id):
    permissions = []
    if user_id in users.user_telegram_ids:
        permissions.append(PERMISSIONS['REGISTERED'])
    else:
        permissions.append(PERMISSIONS['NOT_REGISTERED'])

    if user_id in users.admin_telegram_ids:
        permissions.append(PERMISSIONS['ADMIN'])

    return permissions


def set_permissions(func):
    def wrapped(*args, **kwargs):
        [self, bot, update] = args
        user_id = get_chat_id(update)
        state = kwargs['state']
        state.set_permissions(add_permissions_by_user_id(user_id))
        return func(*args, **kwargs)

    return wrapped
