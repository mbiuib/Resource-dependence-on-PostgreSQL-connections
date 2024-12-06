import threading
import time
from datetime import datetime
import tkinter as tk

import psutil
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

from database import select_stmnt

request = """
SELECT 
    p.name,
    p.lastname,
    p.patronymic,
    p.gender,
    p.birthday,
    pp.number AS passport_number,
    pp.series AS passport_series,
    s.first_number,
    s.second_number,
    s.third_number,
    s.cr
FROM 
    peoples p
LEFT JOIN 
    passports pp ON p.id = pp.people_id
LEFT JOIN 
    snils s ON p.id = s.people_id
WHERE 
    p.gender = 'ж'
ORDER BY 
    p.lastname, p.name
LIMIT 1000 OFFSET (SELECT COUNT(*) FROM peoples) / 2;
"""

# start_t = time.time()
# print(select_stmnt(request))
# print(time.time()-start_t)

# Количество потоков для запроса к БД
THREADS_COUNT = 4
# Количество точек для отображения на графике
POINTS = 40

start_time = time.time()
current_threads = 0

# Листы для хранения данных
timestamps = []
cpu_usage_data = []
memory_usage_data = []
disk_usage_data = []
threads = []


def thread_start():
    global current_threads
    current_threads += 1
    select_stmnt(request)
    current_threads -= 1
    print("quit thread\n\n")


def new_thread():
    t1 = threading.Thread(target=thread_start)
    t1.start()


class Main(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        def on_button_click():
            new_thread()

        # Создаем главное окно приложения
        root = tk.Tk()
        root.title("Добавление потока")
        root.geometry("100x100")

        # Создаем кнопку и привязываем ее к функции on_button_click
        button = tk.Button(root, text="+1 поток", command=on_button_click)
        button.pack(pady=20)

        # Запуск главного цикла обработки событий
        root.mainloop()


def update_data():
    # Добавляем метку времени в секундах от начала работы скрипта
    elapsed_time = time.time() - start_time
    timestamps.append(int(elapsed_time))

    # Собираем данные о ресурсах
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    # Добавляем данные в соответствующие списки
    cpu_usage_data.append(cpu_usage)
    memory_usage_data.append(memory_usage)
    disk_usage_data.append(disk_usage)
    threads.append(current_threads)

    print(cpu_usage_data)
    print(memory_usage_data)
    print(disk_usage_data)
    print(timestamps)
    print()
    print()


m = Main()
m.start()

for i in range(THREADS_COUNT):
    new_thread()

# Настройка графика
plt.ion()  # Включаем интерактивный режим
fig, ax = plt.subplots(4, 1, figsize=(10, 8))
fig.suptitle("Мониторинг ресурсов системы")

while True:
    update_data()

    # Очищаем оси
    for a in ax:
        a.clear()

    # График CPU
    ax[0].plot(timestamps, cpu_usage_data, color="blue", label="CPU Usage (%)")
    ax[0].set_ylim(0, 100)
    ax[0].set_ylabel("CPU Usage (%)")
    ax[0].legend(loc="upper right")

    # График памяти
    ax[1].plot(timestamps, memory_usage_data, color="green", label="Memory Usage (%)")
    ax[1].set_ylim(0, 100)
    ax[1].set_ylabel("Memory Usage (%)")
    ax[1].legend(loc="upper right")

    # График диска
    ax[2].plot(timestamps, disk_usage_data, color="red", label="Disk Usage (%)")
    ax[2].set_ylim(0, 100)
    ax[2].set_ylabel("Disk Usage (%)")
    ax[2].legend(loc="upper right")

    # График потоков
    ax[3].plot(timestamps, threads, color="red", label="Request count")
    ax[3].set_ylim(0, current_threads * 2 - current_threads*0.5)
    ax[3].set_ylabel("Request count")
    ax[3].legend(loc="upper right")

    # Форматирование графиков
    for i in range(len(ax) - 1):  # Настройка для верхних графиков
        ax[i].set_xticks(range(len(timestamps)))  # Сетка по X
        ax[i].xaxis.set_major_locator(MaxNLocator(nbins=10, integer=True))  # Равномерное распределение
        ax[i].set_xticklabels([])  # Убираем подписи времени
        ax[i].grid(True)  # Включаем сетку

    # Настройка для нижнего графика
    ax[3].set_xticks(range(len(timestamps)))
    ax[3].xaxis.set_major_locator(MaxNLocator(nbins=10, integer=True))  # Равномерное распределение
    ax[3].set_xlabel("Time (s)")
    ax[3].grid(True)

    plt.pause(2)  # Обновляем график каждые 5 секунд
    # Выход по Ctrl+C
