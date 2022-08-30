from base.core.connector import Connector


class Migration:

    @staticmethod
    def execute(sql):
        Connector.cursor.execute(sql)
