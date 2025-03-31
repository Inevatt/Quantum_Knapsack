import heapq
from data import allocate_tasks_with_qubo

# Структура события для нашей очереди событий
class Event:
    def __init__(self, time, event_type, payload=None):
        self.time = time          # Время наступления события
        self.event_type = event_type
        self.payload = payload    # Доп. данные (задача или что-то ещё)

    def __lt__(self, other):
        return self.time < other.time


def simulate(tasks, servers, allocation_interval=5.0, simulation_end=100.0):
    # Типы событий
    ARRIVAL = "ARRIVAL"
    DEPARTURE = "DEPARTURE"
    ALLOCATION = "ALLOCATION"
    """
    tasks: список задач (Task) со временем прихода, запросами и пр.
    servers: список серверов (Server)
    allocation_interval: как часто (по времени симуляции) мы вызываем наш алгоритм
    simulation_end: ограничение по времени для демонстрации
    
    Возвращаем статистику: среднее время ожидания, загрузка серверов и т.д.
    """

    # Очередь ожидания задач
    waiting_tasks = []

    # Приоритетная очередь (мин-куча) событий
    event_queue = []

    # Изначально добавляем события ARRIVAL для каждой задачи
    for task in tasks:
        event_queue.append(Event(task.arrival_time, ARRIVAL, task))

    # Добавим первое событие ALLOCATION (потом будем планировать следующие)
    event_queue.append(Event(0.0, ALLOCATION, None))

    heapq.heapify(event_queue)

    # Для логирования метрик
    total_wait_time = 0.0
    completed_tasks = 0

    # Можем отслеживать суммарную загрузку (для вычисления средней загрузки)
    # Упрощённо будем считать, что загрузка не меняется между событиями, 
    # и интегрируем её по времени.
    prev_time = 0.0
    accumulated_memory_usage = [0.0]*len(servers)
    accumulated_ram_usage = [0.0]*len(servers)
    accumulated_cores_usage = [0.0]*len(servers)

    while event_queue:
        event = heapq.heappop(event_queue)
        current_time = event.time

        if current_time > simulation_end:
            break

        # За время delta = current_time - prev_time считаем ресурсную загрузку
        delta = current_time - prev_time
        for i, srv in enumerate(servers):
            accumulated_memory_usage[i] += srv.used_memory * delta
            accumulated_ram_usage[i] += srv.used_ram * delta
            accumulated_cores_usage[i] += srv.used_cores * delta

        prev_time = current_time

        if event.event_type == ARRIVAL:
            # Новая задача приходит -> добавляем в очередь ожидания
            task = event.payload
            waiting_tasks.append(task)

        elif event.event_type == DEPARTURE:
            # Задача завершилась, освобождаем ресурсы
            (task, srv) = event.payload
            srv.free(task)

            # Логирование метрики
            wait_time = (task.start_time - task.arrival_time)
            total_wait_time += wait_time
            completed_tasks += 1

        elif event.event_type == ALLOCATION:
            # Периодически пытаемся распределить задачи
            if waiting_tasks:
                # Вызываем ваш алгоритм (в примере – упрощённый вызов)
                assigned = allocate_tasks_with_qubo(servers, waiting_tasks)
                if (assigned == -1):
                    pass
                else:
                    # Все задачи, которые алгоритм назначил
                    allocated_task_ids = set()
                    print(assigned)
                    for task_idx, srv_idx in assigned:
                        # Обновляем ресурсы
                        current_task = waiting_tasks[task_idx]
                        current_server = servers[srv_idx]

                        current_server.allocate(current_task)
                        current_task.start_time = current_time
                        current_task.finish_time = current_time + current_task.duration
                        allocated_task_ids.add(task_idx)

                        # Создаём событие DEPARTURE
                        departure_event = Event(current_task.finish_time, DEPARTURE, (current_task, current_server))
                        heapq.heappush(event_queue, departure_event)

                    # Удаляем назначенные задачи из waiting_tasks
                    new_w_t = []
                    for i in range(len(waiting_tasks)):
                        if (i not in allocated_task_ids):
                            new_w_t.append(waiting_tasks[i])
                    waiting_tasks = new_w_t

            # Планируем следующее событие ALLOCATION
            heapq.heappush(event_queue, Event(current_time + allocation_interval, ALLOCATION, None))

    # После цикла подсчитываем метрики
    total_time = min(simulation_end, prev_time)
    avg_wait_time = (total_wait_time / completed_tasks) if completed_tasks else 0.0

    # Средняя загрузка (по каждому серверу считаем долю от максимума)
    avg_memory_utilization = []
    avg_ram_utilization = []
    avg_cores_utilization = []
    for i, srv in enumerate(servers):
        avg_mem = accumulated_memory_usage[i] / (srv.total_memory * total_time) if total_time > 0 else 0
        avg_ram = accumulated_ram_usage[i] / (srv.total_ram * total_time) if total_time > 0 else 0
        avg_cores = accumulated_cores_usage[i] / (srv.total_cores * total_time) if total_time > 0 else 0
        avg_memory_utilization.append(avg_mem)
        avg_ram_utilization.append(avg_ram)
        avg_cores_utilization.append(avg_cores)

    return {
        "completed_tasks": completed_tasks,
        "avg_wait_time": avg_wait_time,
        "avg_memory_utilization": avg_memory_utilization,
        "avg_ram_utilization": avg_ram_utilization,
        "avg_cores_utilization": avg_cores_utilization
    }