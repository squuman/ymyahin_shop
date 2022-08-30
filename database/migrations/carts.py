from database.migration import Migration


def up():
    Migration.execute("create table carts(\
        id int primary key AUTO_INCREMENT,\
        product_list text,\
        user_id int,\
        is_open tinyint,\
        FOREIGN key (user_id) REFERENCES users (id)\
    );")
