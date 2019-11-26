from BotStepper.text_messages.Step import Step
from StepHandlers import HandleValueRegexp
from keys import REGISTRATION_KEY, REGISTRATION_ERROR_KEY, MESSAGE_KEY
from config import REGEXP
from bot_redis.storeges import users
from steps.set_step import set_step_start
from permissions.check_permissions import CheckPermissions
from keys import PERMISSIONS
from steps.handler_errors import permission_error
from db.bot_orm.tables.registration_tokens import RegistrationTokens
from db.bot_orm.tables.user import User
from logs import administration_logger


@CheckPermissions([PERMISSIONS['NOT_REGISTERED']], permission_error)
def registration(bot, update, state, props):
    value = props['text']
    translate = props['translate']
    token = RegistrationTokens.get_token(value)
    if token:
        user_telegram = update.message.chat
        user_register = User.create(telegram_id=getattr(user_telegram, 'id', None),
                                    username=getattr(user_telegram, 'username', None),
                                    first_name=getattr(user_telegram, 'first_name', None),
                                    last_name=getattr(user_telegram, 'last_name', None))
        token.use_token(user_register.id)
        users.update()
        state.permissions.append(PERMISSIONS['REGISTERED'])
        administration_logger.info('token was used by %s' % (props['chat_id']))
        return set_step_start(bot, update, state, props)
    administration_logger.warn('nad token %s try used by %s' % (value, props['chat_id']))
    bot.send_message(update.message.chat.id, text=translate([MESSAGE_KEY, REGISTRATION_ERROR_KEY]))


def handle_error(bot, update, state, props):
    translate = props['translate']
    bot.send_message(update.message.chat.id, text=translate([MESSAGE_KEY, REGISTRATION_ERROR_KEY]))


REGISTRATION_STEP = Step(REGISTRATION_KEY, [HandleValueRegexp(REGEXP['REGISTRATION_TOKEN'], registration)],
                         handle_error)
