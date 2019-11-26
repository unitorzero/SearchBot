from BotStepper.inline_messages.InlineMessage import InlineMessage, close_single
from BotStepper.inline_messages.InlineHandler import InlineHandler
from config import PAGINATE_PAGE_LEN
from db.bot_orm.tables.user import User
from utils.generate_msg import users_info
from telegram import InlineKeyboardMarkup


class Users(InlineMessage):
    def __init__(self, state, _id=None):
        super().__init__(state, 'users', _id)
        self.handlers = {
            'left': InlineHandler('left', self._pagination('left')),
            'right': InlineHandler('right', self._pagination())
        }

    def _generate_handlers_btn(self, translate, left=True, right=True, count=5):
        pagination_btns = []
        if left:
            pagination_btns.append(self.handlers['left'].generate_btn('left', translate('prev')))
        if right:
            pagination_btns.append(self.handlers['right'].generate_btn('right', translate('next')))
        self.handlers_btn = [pagination_btns]
        return self

    def _pagination(self, direction='right'):

        def pag(bot, update, state, props):
            data = props['callback_query_data']
            message_id = props['message_id']
            translate = props['translate']
            pagination_params = state.get_inline_msg(message_id).get('params')
            paginate_func = User.paginate_right if direction == 'right' else User.paginate_left
            result = paginate_func(pagination_params['first'], pagination_params['last'])

            if not len(result['result']):
                return bot.editMessageReplyMarkup(chat_id=props['chat_id'], message_id=props['message_id'],
                                                  reply_markup=InlineKeyboardMarkup(
                                                      self._generate_handlers_btn(translate,
                                                                                  data['v'] != 'left',
                                                                                  data['v'] != 'right',
                                                                                  pagination_params[
                                                                                      'count']).handlers_btn))

            dicts = result['result']
            pagination_params['first'] = dicts[0].id
            pagination_params['last'] = dicts[-1].id

            text = users_info(dicts, pagination_params['count'], translate)
            msg = bot.editMessageText(chat_id=props['chat_id'], message_id=props['message_id'],
                                      text=text, reply_markup=InlineKeyboardMarkup(
                    self._generate_handlers_btn(translate, count=pagination_params['count']).handlers_btn))
            self.params = pagination_params
            self.set_id(msg.message_id)
            self.save()

        return pag

    @close_single
    def send_message(self, bot, update, state, props):
        translate = props['translate']
        chat_id = props['chat_id']
        # try:
        result = User.first_paginate()
        dicts = result['result']
        # if not dicts:
        #     bot.send_message(chat_id, text=translate('empty_result'))

        if len(dicts) < PAGINATE_PAGE_LEN:
            # for dict_p in dicts:
            msg_text = users_info(dicts, len(dicts), translate)
            bot.send_message(update.message.chat_id, text=msg_text)

        if len(dicts) >= PAGINATE_PAGE_LEN:
            count = result['result_count']
            dicts = dicts[:PAGINATE_PAGE_LEN]
            pagination_params = {
                'count': count,
                'first': dicts[0].id,
                'last': dicts[-1].id
            }
            text = users_info(dicts, count, translate)
            msg = bot.send_message(update.message.chat_id, text=text,
                                   reply_markup=InlineKeyboardMarkup(self._generate_handlers_btn(translate, left=False,
                                                                                                 count=
                                                                                                 pagination_params[
                                                                                                     'count']).handlers_btn))
            self.params = pagination_params
            self.set_id(msg.message_id).save()
