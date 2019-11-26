from logs import auth_logger


class CheckPermissions:
    def __init__(self, permissions, error):
        self.permissions = permissions
        self.error = error

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            [bot, update, state, props] = args
            if self.check_permissions(state.permissions):
                fn(*args, **kwargs)
            else:
                telegram_id = props['chat_id']
                auth_logger.warning('permissions denied %s, %s' % (telegram_id, fn.__name__))
                self.error(bot, update, state, props)

        return wrapper

    def check_permissions(self, user_permissions):
        return len(self.permissions + user_permissions) != len(set(self.permissions + user_permissions))
