import datetime
import time
from random import choice, randint

from database import *
from utils import randomword

names = [line.rstrip() for line in open('names.txt', encoding='utf-8')]
lastnames = [line.rstrip() for line in open('lastnames.txt', encoding='utf-8')]
patronymics = [line.rstrip() for line in open('patronymics.txt', encoding='utf-8')]
genders = ['м', 'ж']
family_status = ['married', 'not married']
number = 1031190784

#  42468490


def peoples_generate():
    global number
    _ = (f"('{choice(names)}', "
         f"'{choice(patronymics)}', "
         f"'{choice(lastnames)}', "
         f"'{choice(genders)}',"
         f"'{datetime.date(randint(1900, 2024), randint(1, 12), randint(1, 28))}', "
         f"'{randomword(30)}',"
         f"'+7{number}', "
         f"'{randomword(6) + '.' + randomword(10) + '@gmail.com'}', "
         f"{randint(90, 200)}, "
         f"{randint(40, 200)}, "
         f"'{choice(family_status)}')")
    number += 1

    return _


# 531 510
req_t = time.time()
for i in range(10):
    request = (
        f"INSERT INTO peoples (name, patronymic, lastname, gender, birthday, password, phone, email, height, weight, family_status)"
        f"VALUES {", ".join(peoples_generate() for _ in range(53151))};")

    insert_stmnt(request)

print(time.time()-req_t, '-'*50)

print(select_stmnt("SELECT COUNT(*) FROM peoples;"))
