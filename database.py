import os

from dotenv import load_dotenv
import psycopg2
from psycopg2 import Error

load_dotenv()


def select_stmnt(request: str, values=None):
    connection = None
    cursor = None
    data = None

    try:
        connection = psycopg2.connect(user=os.getenv("USER"),
                                      password=os.getenv("PASSWORD"),
                                      host=os.getenv("HOST"),
                                      port=os.getenv("PORT"),
                                      database=os.getenv("DATABASE"))

        cursor = connection.cursor()
        cursor.execute(request, values)
        data = cursor.fetchall()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL: %s", error)
        data = "error"

    finally:
        if connection is not None:
            cursor.close()
            connection.close()
        return data


def insert_stmnt(request: str, values=None):
    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(user=os.getenv("USER"),
                                      password=os.getenv("PASSWORD"),
                                      host=os.getenv("HOST"),
                                      port=os.getenv("PORT"),
                                      database=os.getenv("DATABASE"))

        cursor = connection.cursor()
        cursor.execute(request, values)
        connection.commit()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
