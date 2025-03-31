import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '../'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import random
from src import data as Data
from src import events as Sim



if __name__ == "__main__":
    random.seed(42)

    # Допустим, у нас есть 3 сервера с разными ресурсами:
    servers = [
        Data.Server(0, total_memory=1000, total_ram=200, total_cores=16),
        Data.Server(1, total_memory=800,  total_ram=256, total_cores=8),
        Data.Server(2, total_memory=1200, total_ram=128, total_cores=32)
    ]

    # Сгенерируем случайные задачи
    # 40 задач, у каждой arrival_time в [0..100]
    tasks = []
    num_tasks = 40
    for i in range(num_tasks):
        arrival = random.uniform(-1, 100)
        duration = random.uniform(5, 20)
        mem_req = random.randint(50, 200)
        ram_req = random.randint(10, 50)
        cores_req = random.randint(1, 5)
        tasks.append(Data.Task(arrival, i, duration, mem_req, ram_req, cores_req))

    # Запускаем симуляцию до времени 100, пересматриваем распределение каждые 15 единиц времени
    stats = Sim.simulate(tasks, servers, allocation_interval=15.0, simulation_end=100.0)

    print("=== РЕЗУЛЬТАТЫ СИМУЛЯЦИИ ===")
    print("Выполнено задач:", stats["completed_tasks"])
    print("Среднее время ожидания в очереди:", round(stats["avg_wait_time"], 2))
    print("Средняя загрузка по памяти:", [round(x, 3) for x in stats["avg_memory_utilization"]])
    print("Средняя загрузка по RAM:", [round(x, 3) for x in stats["avg_ram_utilization"]])
    print("Средняя загрузка по ядрам:", [round(x, 3) for x in stats["avg_cores_utilization"]])
