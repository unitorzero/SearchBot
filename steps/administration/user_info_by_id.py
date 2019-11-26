from keys import PERMISSIONS
from steps.handler_errors import permission_error
from permissions.check_permissions import CheckPermissions
from InlineMessages.types.UserInfo import UserInfo


@CheckPermissions([PERMISSIONS['ADMIN']], permission_error)
def user_info(bot, update, state, props):
    info = UserInfo(state)
    info.send_message(bot, update, state, props)
