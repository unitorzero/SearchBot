from BotStepper.inline_messages.InlineMessage import InlineMessage, close_single
from BotStepper.inline_messages.InlineHandler import InlineHandler
from keys import FILTERS_KEYS, CALLBACK_QUERY_DELETE_ALL_FILTERS_KEY, MESSAGE_KEY, CALLBACK_QUERY_DELETE_FILTER_KEY, \
    EMPTY_FILTERS
from utils.generate_msg import generate_message_filters
from BotStepper.utils.utils import get_chat_id
from telegram import InlineKeyboardMarkup


class FiltersInlineMessage(InlineMessage):
    def __init__(self, state, _id=None):
        super().__init__(state, 'filters', _id)
        self.handlers = {
            'del': InlineHandler('del', self.handle_delete_filter),
            CALLBACK_QUERY_DELETE_ALL_FILTERS_KEY: InlineHandler(CALLBACK_QUERY_DELETE_ALL_FILTERS_KEY,
                                                                 self.handle_delete_all_filters)
        }
        self.handlers_btn = []

    def _generate_handlers_btn(self, translate, filters):
        for filter_key, filter_value in FILTERS_KEYS.items():
            filter_obj = filters.get(filter_value)
            if filter_obj:
                self.handlers_btn.append(self.handlers['del'].generate_btn(filter_value, '%s %s' % (
                translate('clear'), translate(filter_value).lower())))

        if len(self.handlers_btn):
            self.handlers_btn.append(self.handlers[CALLBACK_QUERY_DELETE_ALL_FILTERS_KEY].generate_btn('', translate(
                [MESSAGE_KEY, CALLBACK_QUERY_DELETE_ALL_FILTERS_KEY])))

        return self

    def handle_delete_all_filters(self, bot, update, state, props):
        state.clear_filters()
        state.save()
        translate = props['translate']
        message_id = props['message_id']
        bot.editMessageText(text=translate([MESSAGE_KEY, CALLBACK_QUERY_DELETE_FILTER_KEY]),
                            chat_id=update.callback_query.message.chat.id,
                            message_id=self._id
                            )
        state.del_inline_msg(message_id).save()

    def handle_delete_filter(self, bot, update, state, props):
        data = props['callback_query_data']
        translate = props['translate']
        message_id = props['message_id']
        state.delete_filter(data['v'])
        filters = state.get_filters()
        btns = list(map(lambda x: [x], self._generate_handlers_btn(translate, state.get_filters()).handlers_btn))
        if not len(btns):
            state.del_inline_msg(message_id)
        state.save()
        bot.editMessageText(text=generate_message_filters(translate, filters) or translate(EMPTY_FILTERS),
                            chat_id=update.callback_query.message.chat.id,
                            message_id=update.callback_query.message.message_id,
                            reply_markup=InlineKeyboardMarkup(btns))

    @close_single
    def send_message(self, bot, update, state, props):
        translate = props['translate']
        text = generate_message_filters(translate, state.get_filters()) or translate(EMPTY_FILTERS)
        btns = list(map(lambda x: [x], self._generate_handlers_btn(translate, state.get_filters()).handlers_btn))
        msg = bot.send_message(get_chat_id(update), text=text, reply_markup=InlineKeyboardMarkup(btns))
        if len(btns):
            self.set_id(msg.message_id)
            self.save()
