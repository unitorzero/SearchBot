class Step:
    def __init__(self, mark: str, handlers, error):
        self.mark = mark
        self.handlers = handlers
        self.error = error

    def handle(self, bot, update, state, props):
        for handler in self.handlers:

            if handler.middlewares:
                for middleware in handler.middlewares:
                    bot, update, state, props = middleware(bot, update, state, props)

            if handler.check(props):
                handler.success(bot, update, state, props)
                return None
        return self.error(bot, update, state, props)

    def error(self, bot, update, state, props):
        self.error(bot, update, state, props)
