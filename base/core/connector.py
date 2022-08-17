import pymysql


class Connector:
    connector = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='ymyahin_shop',
    )
    cursor = connector.cursor()
