from database.migration import Migration


def up():
    Migration.execute("create table orders(\
        id int primary key AUTO_INCREMENT,\
        user_id int,\
        products text,\
        sum bigint,\
        FOREIGN key (user_id) REFERENCES users (id)\
    );")
