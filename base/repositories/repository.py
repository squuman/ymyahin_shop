from base.core.connector import Connector


class Repository:
    connector = Connector.connector
    sql_cursor = Connector.cursor
    table = None
    model = None

    def get_data(self, additional_condition=""):
        self.sql_cursor.execute(f"SELECT * FROM {self.table} " + additional_condition)

        return self.sql_cursor.fetchall()

    def insert_data(self, values: list):
        fields = ",".join(self.model.fields)
        values = ",".join(values)

        print(f"INSERT INTO {self.table}({fields}) values({values})")
        self.sql_cursor.execute(f"INSERT INTO {self.table}({fields}) values({values})")
        self.connector.commit()

        return self.sql_cursor.rowcount

    def update_data(self):
        pass
