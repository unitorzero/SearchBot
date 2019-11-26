from BotStepper.text_messages.StepHandler import HandleValue


class HandleValueRegexp(HandleValue):
    def __init__(self, value, action, middlewares=[]):
        super().__init__(value, action, middlewares)

    def check(self, props):
        value = props['text']
        return self.value.match(str(value))


class HandleDocument(HandleValue):
    def __init__(self, value, action, middlewares=[]):
        super().__init__(value, action, middlewares)

    def check(self, props):
        return props['document']
