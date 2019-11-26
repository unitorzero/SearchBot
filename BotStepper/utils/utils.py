import json


def get_chat_id(update):
    try:
        chat_id = update.message.chat_id
    except AttributeError:
        chat_id = update.callback_query.message.chat.id

    return chat_id


def get_message_id(update):
    return update.callback_query.message.message_id


def get_message_text(update):
    try:
        text = update.message.text
    except AttributeError:
        text = None
    return text


def get_callback_query_data(update):
    try:
        data = update.callback_query.data
        data = json.loads(data)
    except AttributeError:
        data = None
    return data
