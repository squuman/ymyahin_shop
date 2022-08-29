import pymysql


class Connector:
    connector = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='ymyahin_shop',
    )
    cursor = connector.cursor()
