from BotStepper.utils.utils import get_chat_id


class UserState:
    def __init__(self, redis, state):
        self.redis = redis
        self.state = state

    def __call__(self, fn):
        def wrapped(*args, **kwargs):
            [this, bot, update] = args
            user_id = get_chat_id(update)
            state = self.state(self.redis, user_id)
            fn(*args, **kwargs, state=state)

        return wrapped
