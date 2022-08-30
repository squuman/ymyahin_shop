import pymysql
from config import config


class Connector:
    connector = pymysql.connect(
        host=config.HOST,
        user=config.USER,
        password=config.PASSWORD,
        db=config.DATABASE,
    )
    cursor = connector.cursor()
