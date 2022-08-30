# try:
#     from database.migrations import users, products, orders, carts
#
#     users.up()
#     products.up()
#     orders.up()
#     carts.up()
# except Exception as e:
#     print(e)

try:
    from database.fakers import users, products, orders, carts

    users.fill(30)
    products.fill(30)
    orders.fill(30)
    carts.fill(30)
except Exception as e:
    print(e)
