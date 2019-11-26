
from steps.administration.administration import ADMINISTRATION_STEP
from steps.registration import REGISTRATION_STEP

from keys import COMMAND_START_KEY, ADMINISTRATION_KEY, REGISTRATION_KEY
from steps.start import START_STEP

from steps.administration.add_description import ADD_DESCRIPTION_STEP




steps = {
    COMMAND_START_KEY: START_STEP,
    ADMINISTRATION_KEY: ADMINISTRATION_STEP,
    ADD_DESCRIPTION_STEP.mark: ADD_DESCRIPTION_STEP,
    REGISTRATION_KEY: REGISTRATION_STEP
}
