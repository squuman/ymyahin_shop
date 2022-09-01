from database.migration import Migration


def up():
    Migration.execute("create table users( \
        id int primary key AUTO_INCREMENT,\
        name varchar(255),\
        telegram_id bigint,\
        nickname varchar(255),\
        is_admin tinyint\
    );")
