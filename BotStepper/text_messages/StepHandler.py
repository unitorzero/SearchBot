class HandleValue:
    def __init__(self, value, action, middlewares=[]):
        self.value = value
        self.value_action = action
        self.middlewares = middlewares

    def check(self, props):
        value = props['text']
        valid = self._valid(value)
        if not valid:
            return valid
        return value in self.value

    def _valid(self, value):
        return True

    def success(self, bot, update, state, value):
        self.value_action(bot, update, state, value)
