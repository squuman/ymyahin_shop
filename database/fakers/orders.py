import random
import json
from faker import Faker
from base.controllers.order_controller import OrderController
from base.controllers.user_controller import UserController
from base.controllers.product_controller import ProductController


def fill(count=10):
    controller = OrderController()
    user_controller = UserController()
    product_controller = ProductController()

    users_list = user_controller.get()
    product_list = product_controller.get()

    for _ in range(count):
        cart_list = []
        total_price = 0

        for _ in range(random.randint(0, 3)):
            product = random.choice(product_list)
            amount = random.randint(1, len(product_list))
            total_price += amount * product[2]
            cart_list.append({
                "id": random.choice(product_list),
                'amount': amount
            })

        controller.create([
            f"\"{str(random.choice(users_list)[0])}\"",
            f"\'{str(json.dumps(cart_list))}\'",
            f"\"{str(total_price)}\"",
        ])
