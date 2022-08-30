from database.migration import Migration


def up():
    Migration.execute("create table products(\
    id int primary key AUTO_INCREMENT, \
        name varchar(255),\
        price int,\
        description text\
    );")
