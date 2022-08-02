import pymysql
from pymysql.cursors import DictCursor


class Connector:
    connector = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='ymyahin_shop',
    )
