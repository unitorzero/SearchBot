from json import dumps
from UserState import UserStateInfo
from BotStepper.utils.utils import get_chat_id
from telegram import InlineKeyboardMarkup


def close_single(func):
    def wrapped(self, bot, update, state: UserStateInfo, props):
        del_msg = []

        for key, value in state.get_inline_msg_all().items():
            if value.get('type') == self.type:
                del_msg.append(key)
        state.update_inline_msg()
        chat_id = get_chat_id(update)
        for _id in del_msg:
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=_id, reply_markup=InlineKeyboardMarkup([[]]))
            state.del_inline_msg(_id)
        state.save()
        func(self, bot, update, state, props)

    return wrapped


class InlineMessage:

    def __init__(self, state: UserStateInfo, type='', _id=None):
        self.state = state
        self.type = type
        self.params = {}
        self.handlers = {}
        self._id = _id

    def set_id(self, _id):
        self._id = str(_id)
        return self

    def __call__(self, bot, update, state, props):
        data = props['callback_query_data']
        pass
        if not self.handlers.get(data['mk']):
            pass  # error
        handler = self.handlers.get(data['mk'])
        handler.handle(bot, update, state, props)

    def __str__(self):
        return dumps({'id': self._id, 'type': self.type, 'params': self.params})

    @close_single
    def send_message(self, bot, update, state, props):
        pass

    def save(self):
        self.state.set_inline_msg(self._id, str(self)).save()

    def delete_msg(self, _id):
        self.state.del_inline_msg(_id).save()
