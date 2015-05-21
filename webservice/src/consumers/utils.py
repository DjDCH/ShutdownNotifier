import string
import random


class Generator:
    @staticmethod
    def generate_username(size=30, chars=string.ascii_lowercase + string.digits):
        return Generator.generate(size, chars)

    @staticmethod
    def generate_code(size=6, chars=string.digits):
        return Generator.generate(size, chars)

    @staticmethod
    def generate(size, chars):
        return ''.join(random.choice(chars) for _ in range(size))
