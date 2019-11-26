import redis

from middlewares.write_action import write_action
from permissions.set_permissions import set_permissions
from BotStepper.middlewares.props import Props as props
from BotStepper.middlewares.UserState import UserState as set_state
from UserState import UserStateInfo as UserState

from steps.main import steps

from config import REDIS_CONFIG
from InlineMessages.InlineHandlers import InlineHandlers
from translations.translations import translate
from steps.full_info_by_id import full_info
from steps.set_step import set_step_start
from steps.administration.user_info_by_id import user_info
import logging
from UserState import UserStateInfo
import telegram

Redis = redis.Redis(**REDIS_CONFIG)


class InfoBot:

    @write_action
    @set_state(Redis, UserState)
    @set_permissions
    @props(translate)
    def start(self, bot, update, state: UserStateInfo, props):
        set_step_start(bot, update, state, props)
        logging.info('try start %s' % state.user)

    @write_action
    @set_state(Redis, UserState)
    @set_permissions
    @props(translate)
    def text_handler(self, bot, update, state, props):
        step = steps[state.step]
        logging.info('%s step handle %s' % (state.step, props['text']))
        step.handle(bot, update, state, props)

    @write_action
    @set_state(Redis, UserState)
    @set_permissions
    @props(translate)
    def inline_handler(self, bot, update, state, props):
        InlineHandlers.handle(bot, update, state, props)

    @write_action
    @set_state(Redis, UserState)
    @set_permissions
    @props(translate)
    def command_id_handler(self, bot, update, state, props):
        logging.info('handle command %s', props['text'])
        full_info(bot, update, state, props)

    @write_action
    @set_state(Redis, UserState)
    @set_permissions
    @props(translate)
    def command_user_id_handler(self, bot, update, state, props):
        logging.info('handle command %s', props['text'])
        user_info(bot, update, state, props)

    @write_action
    @set_state(Redis, UserState)
    @set_permissions
    @props(translate)
    def document_handler(self, bot, update, state, props):
        logging.info('handle document ')
        step = steps[state.step]
        #bot.get_file(file_id=update['message']['document']['file_id']).download_as_bytearray().decode("utf-8")
        step.handle(bot, update, state, props)
