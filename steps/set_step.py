from telegram import ReplyKeyboardRemove
from keys import COMMAND_MENU_KEY, ADMINISTRATION_KEY, PERMISSIONS, REGISTRATION_KEY, MESSAGE_KEY, CHOOSE_FILTER
from permissions.check_permissions import CheckPermissions
from keyboards.keyboards import administration_keyboard,  menu_keyboard
from steps.handler_errors import permission_error, permission_error_admin
from utils.generate_msg import generate_message_filters


@CheckPermissions([PERMISSIONS['REGISTERED']], permission_error)
def set_step_start(bot, update, state, props):
    from steps.start import START_STEP
    translate = props['translate']
    bot.send_message(chat_id=update.message.chat_id, text=translate([MESSAGE_KEY, COMMAND_MENU_KEY]),
                     reply_markup=menu_keyboard(translate, state.permissions))
    state.set_step(START_STEP.mark).save()


@CheckPermissions([PERMISSIONS['ADMIN']], permission_error_admin)
def set_step_administration(bot, update, state, props):
    from steps.administration.administration import ADMINISTRATION_STEP
    translate = props['translate']
    bot.send_message(update.message.chat_id,
                     text=translate([MESSAGE_KEY, ADMINISTRATION_KEY]),
                     reply_markup=administration_keyboard(translate, [PERMISSIONS['ADMIN']]))
    state.set_step(ADMINISTRATION_STEP.mark).save()


@CheckPermissions([PERMISSIONS['NOT_REGISTERED']], False)
def set_step_registration(bot, update, state, props):
    from steps.registration import REGISTRATION_STEP
    translate = props['translate']
    bot.send_message(update.message.chat_id, text=translate([MESSAGE_KEY, REGISTRATION_KEY]),
                     reply_markup=ReplyKeyboardRemove())
    state.set_step(REGISTRATION_STEP.mark).save()


@CheckPermissions([PERMISSIONS['REGISTERED']], permission_error)
def set_step_extended_search(bot, update, state, props):
    from steps.extended_search.search import SEARCH_STEP
    translate = props['translate']
    text = generate_message_filters(translate, state.get_filters())
    bot.send_message(update.message.chat_id, text=text or translate(CHOOSE_FILTER),
                     reply_markup=filters_keyboard(translate, state.permissions))
    state.set_step(SEARCH_STEP.mark).save()


@CheckPermissions([PERMISSIONS['ADMIN']], permission_error_admin)
def set_step_pack_search(bot, update, state, props):
    from steps.pack_search.search import PACK_SEARCH_STEP
    translate = props['translate']
    chat_id = props['chat_id']
    text = translate(PACK_SEARCH_STEP.mark)
    bot.send_message(chat_id, text=text, reply_markup=packet_search_keyboard(translate, state.permissions, {}))
    state.set_step(PACK_SEARCH_STEP.mark).save()


@CheckPermissions([PERMISSIONS['REGISTERED']], permission_error)
def set_step_search(bot, update, state, props):
    from steps.search.search import SIMPLE_SEARCH_STEP
    translate = props['translate']
    text = translate('choose_filter')
    bot.send_message(update.message.chat_id, text=text,
                     reply_markup=simple_filters_keyboard(translate, state.permissions))
    state.set_step(SIMPLE_SEARCH_STEP.mark).save()
