from db.bot_orm.tables.user import User
import logging


class Users:
    log = logging

    def __init__(self):
        self.UserTable = User
        self.users = []
        self.user_ids = []
        self.user_telegram_ids = []
        self.admins = []
        self.admin_ids = []
        self.admin_telegram_ids = []

        self.update()

    def __str__(self):
        return '\r\nusers: %s \r\n\r\nadmins: %s\r\n' % (list(map(str, self.users)), list(map(str, self.admins)))

    def update(self):
        self.users = self.UserTable.all()
        self.admins = list(filter(lambda x: x.admin, self.users))

        self.user_ids = list(map(lambda x: x.id, self.users))
        self.user_telegram_ids = list(map(lambda x: x.telegram_id, self.users))
        self.admin_ids = list(map(lambda x: x.id, self.admins))
        self.admin_telegram_ids = list(map(lambda x: x.telegram_id, self.admins))
        self.log.info('Storage Users was updated. \r\n%s' % self)
        return self

    def get_user_by_telegram_id(self, _id):
        items = list(filter(lambda x: x.telegram_id == _id, self.users))
        return items[0] if len(items) else False

    def get_user_by_id(self, _id):
        items = list(filter(lambda x: x.id == int(_id), self.users))
        return items[0] if len(items) else False

    def get_admin_by_id(self, _id):
        items = list(filter(lambda x: x.id == _id, self.admins))
        return items[0] if len(items) else False

    def get_admin_by_telegram_id(self, _id):
        items = list(filter(lambda x: x.telegram_id == _id, self.admins))
        return items[0] if len(items) else False

    def delete_user(self, _id):
        User.delete(_id)
        user = self.get_user_by_id(_id)
        self.log.warning('User |%s| was deleted.' % user)
        self.update()
        return user

    def set_description(self, _id, description):
        User.add_description(_id, description)
        self.update()
        user = self.get_user_by_id(_id)
        self.log.warning('User |%s| set decription %s.' % (user, description))
        return user


users = Users()
