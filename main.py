from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, RegexHandler
from config import BOT_TOKEN, BOT_ID_HANDLE_PATTERN, USER_ID_HANDLE_PATTERN, PROD_MODE
import logging
from logs import errors_file_handler
import multiprocessing

logging.basicConfig(
    format='%(asctime)s|%(levelname)s| %(message)s',
    level=logging.INFO if not PROD_MODE else logging.WARN,
    handlers=[errors_file_handler, logging.StreamHandler()])

from keys import BOT_COMMAND
from InfoBot import InfoBot

logging.info('project run')

updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher
InfoBot = InfoBot()

logging.info('init InfoBot, telegram dispatcher')

command_start_handler = CommandHandler(BOT_COMMAND['START'], InfoBot.start)
message_text_handler = MessageHandler(Filters.text, InfoBot.text_handler)
inline_query_handler = CallbackQueryHandler(InfoBot.inline_handler)
command_id_handler = RegexHandler(BOT_ID_HANDLE_PATTERN, InfoBot.command_id_handler)
command_user_handler = RegexHandler(USER_ID_HANDLE_PATTERN, InfoBot.command_user_id_handler)
document_handler = MessageHandler(Filters.document, InfoBot.document_handler)

dispatcher.add_handler(command_start_handler)
dispatcher.add_handler(message_text_handler)
dispatcher.add_handler(inline_query_handler)
dispatcher.add_handler(command_id_handler)
dispatcher.add_handler(command_user_handler)
dispatcher.add_handler(document_handler)

logging.info("=" * 10 + ' add handlers, start polling, start pool with ' + str(
    len(multiprocessing.active_children())) + ' process ' + "=" * 10)

updater.start_polling()
