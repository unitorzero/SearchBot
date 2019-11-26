from InlineMessages.types.Filters import FiltersInlineMessage
from InlineMessages.types.Search import SearchInlineMessage
from InlineMessages.types.Users import Users
from InlineMessages.types.UserInfo import UserInfo
from UserState import UserStateInfo
import logging


class InlineHandlers:
    types = {
        'filters': FiltersInlineMessage,
        'search': SearchInlineMessage,
        'users': Users,
        'user_info': UserInfo
    }

    @staticmethod
    def handle(bot, update, state: UserStateInfo, props):
        message_id = props['message_id']
        msg = state.get_inline_msg(message_id)
        if not msg or not InlineHandlers.types.get(msg.get('type')):
            logging.warning('inline %s handler don`t exist' % (msg.get('type')))
            return
        handler = InlineHandlers.types.get(msg.get('type'))(state, _id=message_id)
        logging.info('inline %s handler handle %s' % (msg.get('type'), props['callback_query_data']))
        handler(bot, update, state, props)
