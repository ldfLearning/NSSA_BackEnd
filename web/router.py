from web import settings

DATABASE_MAPPING = settings.DATABASE_APPS_MAPPING
print('DATABASE_MAPPING = {}'.format(DATABASE_MAPPING))


class DatabaseAppsRouter(object):

    # 设置 应用app 读取时数据库的设置
    def db_for_read(self, model, **hints):
        if model._meta.app_label in DATABASE_MAPPING:
            return DATABASE_MAPPING[model._meta.app_label]
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in DATABASE_MAPPING:
            return DATABASE_MAPPING[model._meta.app_label]
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure that apps only appear in the related database.
        根据app_label的值只在相应的数据库中创建一个表，如果删除该def或
        不指定过滤条件，则一个Model会在每个数据库里都创建一个表。
        """
        if db in DATABASE_MAPPING.values():
            return DATABASE_MAPPING.get(app_label) == db
        elif app_label in DATABASE_MAPPING:
            return False
        return None
