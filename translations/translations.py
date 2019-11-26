from BotStepper.utils.Translate import Translate
from config import DEFAULT_LOCALE
import os

locals = {
    'ua': os.path.join(os.path.dirname(os.path.realpath(__file__)), './locals/ua.json')
}

translate = Translate(locals, DEFAULT_LOCALE)
