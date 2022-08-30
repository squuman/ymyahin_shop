from faker import Faker
import random
from base.controllers.user_controller import UserController


def fill(count=10):
    controller = UserController()
    faker = Faker()

    for _ in range(count):
        # print()
        controller.create([
            f"\"{faker.name()}\"",
            f"\"{str(random.randint(0, 99999999))}\"",
            f"\"{faker.word()}\"",
            f"\"{str(0)}\"",
        ])
