from BotStepper.text_messages.Step import Step
from BotStepper.text_messages.StepHandler import HandleValue
from keys import ADMINISTRATION_GENERATE_TOKEN_KEY, COMMAND_MENU_KEY, ADMINISTRATION_KEY, \
    ADMINISTRATION_ACTIVE_TOKENS_KEY, PERMISSIONS, MESSAGE_KEY, USERS
from steps.set_step import set_step_start
import redis
from config import REDIS_CONFIG
from permissions.check_permissions import CheckPermissions
from steps.handler_errors import permission_error_admin
from translations.translations import translate
from db.bot_orm.tables.registration_tokens import RegistrationTokens
from bot_redis.storeges import users
from steps.handler_errors import bad_input_error
from logs import administration_logger
from InlineMessages.types.Users import Users
import datetime

Redis = redis.Redis(**REDIS_CONFIG)

permissions = [PERMISSIONS['ADMIN']]


@CheckPermissions(permissions, permission_error_admin)
def generate_registration_key(bot, update, state, props):
    translate = props['translate']
    created_user = users.get_admin_by_telegram_id(props['chat_id'])
    if not created_user:
        return administration_logger.error('access denied, admin with telegram_id "%s" not find' % (props['chat_id']))
        # raise Exception('access denied, admin with telegram_id "%s" not find' % (props['chat_id']))

    token = RegistrationTokens.add_token(created_user.id)
    administration_logger.warning('new token, created by %s' % state.user)
    bot.send_message(update.message.chat_id, text='%s: \r\n%s' % (translate('token_for_registration'), token.token))


@CheckPermissions(permissions, permission_error_admin)
def active_tokens_key(bot, update, state, props):
    translate = props['translate']
    tokens_db = RegistrationTokens.get_unused_tokens()
    tokens = [{'token': token.token, 'time': token.fresh_until - datetime.datetime.now()} for token in tokens_db]
    if tokens:
        result = []
        for item in tokens:
            result.append('%s \r\n %s %s' % (item['token'], translate('end_to'), str(item['time']).split('.')[0]))
        return bot.send_message(update.message.chat_id, text='%s %s' % (
        translate([MESSAGE_KEY, ADMINISTRATION_ACTIVE_TOKENS_KEY]), '\r\n'.join(result)))

    bot.send_message(update.message.chat_id,
                     text=translate('active_tokens_dont_exist'))


@CheckPermissions(permissions, permission_error_admin)
def show_users(bot, update, state, props):
    users_obj = Users(state)
    users_obj.send_message(bot, update, state, props)


ADMINISTRATION_STEP = Step(ADMINISTRATION_KEY,
                           [HandleValue(translate.all(ADMINISTRATION_GENERATE_TOKEN_KEY), generate_registration_key),
                            HandleValue(translate.all(ADMINISTRATION_ACTIVE_TOKENS_KEY), active_tokens_key),
                            HandleValue(translate.all(USERS), show_users),
                            HandleValue(translate.all(COMMAND_MENU_KEY), set_step_start)], bad_input_error)
