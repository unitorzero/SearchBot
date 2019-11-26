from BotStepper.text_messages.Step import Step
from BotStepper.text_messages.StepHandler import HandleValue
from StepHandlers import HandleValueRegexp
from keys import USERS_ADD_DESCRIPTION, ADMINISTRATION_KEY, PERMISSIONS
from steps.handler_errors import bad_input_error
from steps.set_step import set_step_administration
from translations.translations import translate
from config import REGEXP
from bot_redis.storeges import users
from steps.set_step import set_step_administration
from utils.generate_msg import update_description
from permissions.check_permissions import CheckPermissions
from steps.handler_errors import permission_error_admin

permissions = [PERMISSIONS['ADMIN']]


@CheckPermissions(permissions, permission_error_admin)
def add_description(bot, update, state, props):
    description = props['text']
    chat_id = props['chat_id']
    translate = props['translate']
    user_id = state.step_params.get('user_id')
    user = users.get_user_by_id(user_id)
    if not user:
        bot.send_message(chat_id, text=translate('user_not_found'))
        return set_step_administration(bot, update, state, props)
    user = users.set_description(user.id, description)
    text = update_description(translate, user)
    bot.send_message(chat_id, text=text)
    set_step_administration(bot, update, state, props)


ADD_DESCRIPTION_STEP = Step(USERS_ADD_DESCRIPTION,
                            [HandleValue(translate.all(ADMINISTRATION_KEY), set_step_administration),
                             HandleValueRegexp(REGEXP['DESCRIPTION'], add_description),
                             ], bad_input_error)
