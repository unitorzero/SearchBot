from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from keys import COMMAND_MENU_KEY, ADMINISTRATION_GENERATE_TOKEN_KEY, ADMINISTRATION_ACTIVE_TOKENS_KEY, \
    SHOW_FILTERS_KEY
from json import dumps
from telegram import ReplyKeyboardMarkup, KeyboardButton
from keys import SEARCH_KEY, COMMAND_MENU_KEY, ADMINISTRATION_KEY, MESSAGE_KEY, SIMPLE_SEARCH_KEY, EXTENDED_SEARCH_KEY


class StepKeyboard:

    def __init__(self, dict_keys, generate_schema):
        self.dict_keys = dict_keys
        self._generate_schema = generate_schema

    def generate_schema(self, translation, permissions, params):
        return self._generate_schema(translation, permissions, params)

    def __call__(self, translation, permissions, params={}):
        schema = self.generate_schema(translation, permissions, params)
        keyboard = []
        keyboard_row = []
        for row in schema:
            for text_key in row:
                if isinstance(text_key, int):
                    keyboard_row.append(
                        KeyboardButton(text=translation(self.dict_keys[text_key])))  # TODO raise invalid schema
                else:
                    keyboard_row.append(text_key)
            keyboard.append(keyboard_row)
            keyboard_row = []
        return ReplyKeyboardMarkup(keyboard)



def generate_menu_schema(translation, permissions, params):
    schema = [[0]]
    if PERMISSIONS['ADMIN'] in permissions:
        schema.append([1])

    return schema


back_to_menu_keyboard = StepKeyboard({0: COMMAND_MENU_KEY, 1: PATTERN_KEY, 2: SIMPLE_SEARCH_KEY},
                                     generate_back_to_menu_schema)


def generate_simple_back_to_menu_schema(translation, permissions, params={}):
    return [[0]]


simple_back_to_menu_keyboard = StepKeyboard({0: COMMAND_MENU_KEY}, generate_simple_back_to_menu_schema)

menu_keyboard = StepKeyboard({0: SEARCH_KEY, 1: ADMINISTRATION_KEY}, generate_menu_schema)


def generate_administration_schema(translation, permissions, params):
    return [[0, 1], [3], [2]]


administration_keyboard = StepKeyboard({0: [ADMINISTRATION_GENERATE_TOKEN_KEY],
                                        1: [ADMINISTRATION_ACTIVE_TOKENS_KEY],
                                        2: [COMMAND_MENU_KEY],
                                        3: [USERS]}, generate_administration_schema)


def generate_filters_schema(translation, permissons, params):
    return [[0, 1], [2, 13, 14, 15], [8, 16], [3, 4, 5], [6, 7, 12], [11], [10], [9]]



def generate_simple_filters_schema(translation, permissions, params):
    search = [6]
    if PERMISSIONS['ADMIN'] in permissions:
        search.append(8)
    return [[3, 0, 1], [4, 5], search, [7]]


def only_administration_schema(translation, permissons, params):
    return [[0]]


only_administration = StepKeyboard({0: ADMINISTRATION_KEY}, only_administration_schema)

def only_menu_schema(translation, permissons, params):
    return [[0]]


only_menu = StepKeyboard({0: COMMAND_MENU_KEY}, only_menu_schema)


def pagination(step=0):
    keyboard = []
    if step:
        keyboard.append(
            InlineKeyboardButton(text='Left', callback_data=dumps({'option': 'pagination', 'value': 'left'})))
    keyboard.append(
        InlineKeyboardButton(text='Right', callback_data=dumps({'option': 'pagination', 'value': 'right'})))
    return InlineKeyboardMarkup([keyboard])
