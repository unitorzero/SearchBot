from keys import (
    MESSAGE_KEY,
    FILTER_ADDED,
    UNKNOWN_ERROR_KEY,
    DB_ERROR_QUERY_CANCELED_KEY,
    USERS_ADD_DESCRIPTION,
    USERS_UPDATE_DESCRIPTION,
    DESCRIPTION
)
from psycopg2 import errors as dbapi_errors
from sqlalchemy import exc as alchemy_errors
from config import PAGINATE_MAX_LEN


def filter_added(translate, filter, value):
    return translate([MESSAGE_KEY, FILTER_ADDED]) % (str(translate(filter)).lower(), value)


def generate_message_filters(translate, obj):
    head = '%s:\r\n' % (translate('filters'))
    result = ''
    filters = FILTERS_KEYS.values()
    for filter in filters:
        value_obj = obj.get(filter, None)
        if value_obj:
            result += '%s: %s \r\n' % (translate(filter), value_obj['value'] if filter != 'id' else value_obj)

    return head + result if result else ''


def set_value_if_exist(value, label):
    return '%s: %s' % (label, value) if value else ''


def get_if_exist(obj, first, second):
    first_value = obj.get(first)
    return first_value if first_value else obj.get(second)


def set_list_values(values):
    if not values:
        return ''
    return ', '.join(list(filter(lambda x: x, set(values))))


def set_connexions(connexions):
    connexions = list(filter(lambda x: x, connexions))
    connexions = dicts_set_by_values(connexions)
    result = ''
    if len(connexions):
        for conn in connexions:
            result += '/id_%s - %s\r\n' % (conn['id2'], conn['type'])
        return result
    return False


def dicts_set_by_values(items):
    hashes = []
    result_list = []
    for item in items:
        item_hash = hash(frozenset(item.values()))
        if item_hash not in hashes:
            hashes.append(item_hash)
            result_list.append(item)
    return result_list


def concat_group(group):
    group = list(filter(lambda x: x, group))
    return '\r\n' + '\r\n'.join(group) + '\r\n' if group else ''



def users_info(users, count, translate):
    message = ''
    message += '%s: %s\r\n' % (translate('count'), '100+' if count > PAGINATE_MAX_LEN else count)
    for user in users:
        link_user = '/user_%s\r\n' % (user.id)
        message += concat_group([
            link_user,
            set_value_if_exist(user.id, translate('id')),
            set_value_if_exist(user.telegram_id, translate('telegram_id')),
            set_value_if_exist(user.username, translate('username')),
            set_value_if_exist(user.first_name, translate('first_name')),
            set_value_if_exist(user.last_name, translate('last_name')),
            set_value_if_exist(str(user.registration).split('.')[0], translate('registration')),
            set_value_if_exist(user.admin, translate('admin')),
            set_value_if_exist(user.description or translate('not_defined'), translate(DESCRIPTION))
        ])
    return message


def user_info(translate, user, requests):
    message = ''
    message += concat_group([
        set_value_if_exist(user.id, translate('id')),
        set_value_if_exist(user.telegram_id, translate('telegram_id')),
        set_value_if_exist(user.username, translate('username')),
        set_value_if_exist(user.first_name, translate('first_name')),
        set_value_if_exist(user.last_name, translate('last_name')),
        set_value_if_exist(str(user.registration).split('.')[0], translate('registration')),
        set_value_if_exist(user.admin, translate('admin')),
        set_value_if_exist(user.description or translate('not_defined'), translate(DESCRIPTION))
    ])

    if requests:
        message += concat_group([translate('requests')])

    for request in requests:
        message += concat_group([
            set_value_if_exist(str(request.date).split('.')[0], translate('request_date')),
            generate_message_filters(translate, request.filters)
        ])

    return message


def user_was_deleted(translate, user):
    message = ''
    message += user_info(translate, user, [])
    message += translate('was_deleted')
    return message


def error_message_text(e, translate):
    key = UNKNOWN_ERROR_KEY
    if isinstance(e, alchemy_errors.DBAPIError) and isinstance(e.orig, dbapi_errors.QueryCanceled):
        key = DB_ERROR_QUERY_CANCELED_KEY
    return translate(key)


def add_user_description(translate, user):
    message = ''
    message += user_info(translate, user, [])
    message += translate([MESSAGE_KEY, USERS_ADD_DESCRIPTION])
    return message


def update_description(translate, user):
    message = ''
    message += user_info(translate, user, [])
    message += translate([MESSAGE_KEY, USERS_UPDATE_DESCRIPTION])
    return message


def csv_was_created_soon(translate, filters):
    message = ''
    message += translate("csv_was_created_soon") + '\r\n'
    message += generate_message_filters(translate, filters)
    return message


def csv_was_created(translate, filters):
    message = ''
    message += translate("csv_was_created") + '\r\n'
    message += generate_message_filters(translate, filters)
    return message


def crate_csv_error(translate, filters):
    message = ''
    message += translate("csv_error") + '\r\n'
    message += generate_message_filters(translate, filters)
    return message
