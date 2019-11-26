from BotStepper.text_messages.Step import Step
from BotStepper.text_messages.StepHandler import HandleValue
from keys import COMMAND_MENU_KEY, PERMISSIONS, \
    MESSAGE_ENTER_KEY, EXTENDED_SEARCH_KEY, SIMPLE_SEARCH_KEY, SIMPLE_FILTERS_KEYS, PACK_SEARCH_KEY
from utils.ValueKeyValue import ValueKeyValue
from keyboards.keyboards import simple_back_to_menu_keyboard
from steps.handler_errors import permission_error
from permissions.check_permissions import CheckPermissions
from steps.set_step import set_step_start, set_step_extended_search as set_step_search, set_step_pack_search
from itertools import chain
from translations.translations import translate
from steps.handler_errors import bad_input_error
from steps.search.filters.Filter import Filter

filters = {}
for filter_key in SIMPLE_FILTERS_KEYS.values():
    filters[filter_key] = translate.all(filter_key)

filters_key_values = ValueKeyValue(filters)


@CheckPermissions([PERMISSIONS['REGISTERED']], permission_error)
def action(bot, update, state, props):
    value = props['text']
    translate = props['translate']
    filter_key = filters_key_values.get_keys(value)[0]
    simple_filter_key = Filter.generate_step_key(filters_key_values.get_keys(value)[0])
    bot.send_message(update.message.chat_id, text=translate([MESSAGE_ENTER_KEY, filter_key]),
                     reply_markup=simple_back_to_menu_keyboard(translate, []))
    state.set_step(simple_filter_key).save()


handle_filters = HandleValue(
    list(chain.from_iterable([translate.all(value) for value in SIMPLE_FILTERS_KEYS.values()])), action)

handle_start = HandleValue(translate.all(COMMAND_MENU_KEY), set_step_start)

handle_set_extended_search = HandleValue(translate.all(EXTENDED_SEARCH_KEY), set_step_search)

handle_set_packet_search = HandleValue(translate.all(PACK_SEARCH_KEY), set_step_pack_search)

SIMPLE_SEARCH_STEP = Step(SIMPLE_SEARCH_KEY, [handle_filters, handle_start, handle_set_extended_search,
                                              handle_set_packet_search],
                          bad_input_error)
