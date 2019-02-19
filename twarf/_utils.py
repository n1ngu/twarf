
import string
import random


def build_random_string(length=32):
    return ''.join(
        random.choice(
            string.digits + string.ascii_letters
        )
        for x in range(length)
    ).encode('ascii')
