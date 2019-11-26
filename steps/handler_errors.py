from keys import AUTH_ERROR, MESSAGE_KEY


def permission_error(bot, update, state, props):
    value = props['text']
    translate = props['translate']
    from steps.set_step import set_step_registration
    bot.send_message(update.message.chat_id, text=translate([MESSAGE_KEY, AUTH_ERROR]))
    set_step_registration(bot, update, state, props)


def permission_error_admin(bot, update, state, props):
    value = props['text']
    translate = props['translate']
    bot.send_message(update.message.chat_id, text=translate([MESSAGE_KEY, AUTH_ERROR]))


def start_step_error(bot, update, state, props):
    value = props['text']
    # bot.send_message()


def bad_input_error(bot, update, state, props):
    translate = props['translate']
    chat_id = props['chat_id']
    text = translate('bad_input_step')
    bot.send_message(chat_id, text=text)
