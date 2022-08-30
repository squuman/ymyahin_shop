from faker import Faker
import random
from base.controllers.product_controller import ProductController


def fill(count=10):
    controller = ProductController()
    faker = Faker()

    for _ in range(count):
        controller.create([
            f"\"{faker.word()}\"",
            f"\"{str(random.randint(0, 99999999))}\"",
            f"\"{faker.text()}\"",
        ])
