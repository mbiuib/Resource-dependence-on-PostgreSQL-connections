from random import randint

from database import *


peoples_count = 1
peoples = 43000000


def passports_generate():
    global peoples_count
    global peoples
    if peoples_count >= peoples:
        return

    _ = (f"({peoples_count}, "
         f"'{randint(100, 999)}',"
         f"'{randint(100, 999)}',"
         f"'{randint(100, 999)}',"
         f"{randint(10, 99)})")
    peoples_count += 1

    return _


for i in range(4300):
    request = (
        f"INSERT INTO snils (people_id, first_number, second_number, third_number, cr)"
        f"VALUES {", ".join(passports_generate() for _ in range(10000))};")

    insert_stmnt(request)
