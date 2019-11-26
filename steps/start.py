from BotStepper.text_messages.Step import Step
from BotStepper.text_messages.StepHandler import HandleValue
from keys import COMMAND_START_KEY, SEARCH_KEY, ADMINISTRATION_KEY
from steps.set_step import set_step_search
from steps.set_step import set_step_administration
from steps.handler_errors import start_step_error
from translations.translations import translate

START_STEP = Step(COMMAND_START_KEY,
                  [HandleValue(translate.all(SEARCH_KEY), set_step_search),
                   HandleValue(translate.all(ADMINISTRATION_KEY), set_step_administration)], start_step_error)
