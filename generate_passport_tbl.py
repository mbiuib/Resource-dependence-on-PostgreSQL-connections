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
         f"'{randint(1000, 9999)}',"
         f"{randint(100000, 999999)})")
    peoples_count += 1

    return _


for i in range(4300):
    request = (
        f"INSERT INTO passports (people_id, number, series)"
        f"VALUES {", ".join(passports_generate() for _ in range(10000))};")

    insert_stmnt(request)
