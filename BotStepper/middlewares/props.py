from utils.properties_telegram import get_chat_id, get_message_text, get_callback_query_data, \
    get_callback_query_message_id, get_document_props


class Props:
    def __init__(self, translate):
        self.translate = translate

    def __call__(self, fn):
        def wrapped(*args, **kwargs):
            [this, bot, update] = args
            state = kwargs.get('state')
            props = {
                'chat_id': get_chat_id(update),
                'text': get_message_text(update),
                'callback_query_data': get_callback_query_data(update),
                'message_id': get_callback_query_message_id(update),
                'document': get_document_props(update),
                'translate': self.translate(state.locale)
            }
            return fn(*args, **kwargs, props=props)

        return wrapped
