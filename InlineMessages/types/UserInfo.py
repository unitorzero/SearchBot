from BotStepper.inline_messages.InlineMessage import InlineMessage, close_single
from BotStepper.inline_messages.InlineHandler import InlineHandler
from config import PAGINATE_PAGE_LEN
from db.bot_orm.tables.requests import Requests
from utils.generate_msg import user_info, user_was_deleted, add_user_description
from telegram import InlineKeyboardMarkup
from config import REGEXP
from db.bot_orm.tables.user import User
from bot_redis.storeges import users
import logging
from keys import USERS_ADD_DESCRIPTION
from bot_redis.storeges import users
from steps.administration.add_description import USERS_ADD_DESCRIPTION, ADD_DESCRIPTION_STEP
from UserState import UserStateInfo
from keyboards.keyboards import only_administration


class UserInfo(InlineMessage):
    log = logging

    def __init__(self, state, _id=None):
        super().__init__(state, 'user_info', _id)
        self.handlers = {
            'left': InlineHandler('left', self._pagination('left')),
            'right': InlineHandler('right', self._pagination()),
            USERS_ADD_DESCRIPTION: InlineHandler(USERS_ADD_DESCRIPTION, self.add_description),
            'delete': InlineHandler('delete', self.delete)
        }

    def _generate_handlers_btn(self, translate, left=True, right=True, count=5):
        pagination_btns = []

        if left and count:
            pagination_btns.append(self.handlers['left'].generate_btn('left', translate('prev')))
        if right and count:
            pagination_btns.append(self.handlers['right'].generate_btn('right', translate('next')))

        self.handlers_btn = [pagination_btns,
                             [self.handlers['delete'].generate_btn('delete', translate('user_delete'))],
                             [self.handlers[USERS_ADD_DESCRIPTION].generate_btn(USERS_ADD_DESCRIPTION,
                                                                                translate(USERS_ADD_DESCRIPTION))]]
        return self

    def add_description(self, bot, update, state: UserStateInfo, props):
        data = props['callback_query_data']
        message_id = props['message_id']
        translate = props['translate']
        chat_id = props['chat_id']
        params = state.get_inline_msg(message_id).get('params')
        user_id = params.get('user_id')
        user = users.get_user_by_id(user_id)

        state.set_step(ADD_DESCRIPTION_STEP.mark)
        state.step_params = {'user_id': user_id}
        state.save()
        bot.send_message(chat_id, text=add_user_description(translate, user),
                         reply_markup=only_administration(translate, state.permissions, {}))

    def delete(self, bot, update, state, props):
        data = props['callback_query_data']
        message_id = props['message_id']
        translate = props['translate']
        chat_id = props['chat_id']
        params = state.get_inline_msg(message_id).get('params')
        user_id = params.get('user_id')
        user = users.delete_user(user_id)
        bot.editMessageText(chat_id=chat_id, message_id=message_id, text=user_was_deleted(translate, user),
                            reply_markup=InlineKeyboardMarkup([]))
        self.delete_msg(message_id)

    def _pagination(self, direction='right'):
        def pag(bot, update, state, props):
            data = props['callback_query_data']
            message_id = props['message_id']
            translate = props['translate']
            pagination_params = state.get_inline_msg(message_id).get('params')
            user = users.get_user_by_id(pagination_params['user_id'])

            paginate_func = Requests.paginate_right if direction == 'right' else Requests.paginate_left

            result = paginate_func(pagination_params['user_id'], pagination_params['first'], pagination_params['last'])

            if not len(result['result']):
                return bot.editMessageReplyMarkup(chat_id=props['chat_id'], message_id=props['message_id'],
                                                  reply_markup=InlineKeyboardMarkup(
                                                      self._generate_handlers_btn(translate,
                                                                                  data['v'] != 'left',
                                                                                  data['v'] != 'right',
                                                                                  pagination_params[
                                                                                      'count']).handlers_btn))

            requests = result['result']
            pagination_params['first'] = requests[0].id
            pagination_params['last'] = requests[-1].id

            text = user_info(translate, user, requests)
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
        value = props['text']

        _id = REGEXP['digits'].search(value).group()
        user = users.get_user_by_id(_id)
        if not user:
            return bot.send_message(chat_id, text=translate('user_not_found'))
        result = Requests.first_paginate(_id)
        requests = result['result']

        first = 0
        last = 0
        count = 0
        if len(requests) > 0:
            requests = requests[:PAGINATE_PAGE_LEN]
            count = result['result_count']
            first = requests[0].id
            last = requests[-1].id

        pagination_params = {
            'user_id': _id,
            'count': count,
            'first': first,
            'last': last
        }
        text = user_info(translate, user, requests)
        msg = bot.send_message(update.message.chat_id, text=text,
                               reply_markup=InlineKeyboardMarkup(self._generate_handlers_btn(translate, left=False,
                                                                                             count=pagination_params[
                                                                                                 'count']).handlers_btn))
        self.params = pagination_params
        self.set_id(msg.message_id).save()
        self.log.info('Show info user %s' % user)
