from Distribution import qubo_solver

class Task:
    def __init__(self, task_id, arrival_time, duration, memory_req, ram_req, cores_req):
        self.task_id = task_id
        self.arrival_time = arrival_time    # Время "появления" задачи в системе
        self.duration = duration            # Время выполнения задачи
        self.memory_req = memory_req
        self.ram_req = ram_req
        self.cores_req = cores_req
        self.start_time = None             # Заполним, когда задача получит ресурсы
        self.finish_time = None            # Заполним, когда задача закончит выполнение

    def __repr__(self):
        return f"<Task {self.task_id} A={self.arrival_time} D={self.duration}>"


class Server:
    def __init__(self, server_id, total_memory, total_ram, total_cores):
        self.server_id = server_id
        self.total_memory = total_memory
        self.total_ram = total_ram
        self.total_cores = total_cores
        # Текущее использование
        self.used_memory = 0
        self.used_ram = 0
        self.used_cores = 0

    def allocate(self, task: Task):
        """Фактическое резервирование ресурсов под задачу."""
        self.used_memory += task.memory_req
        self.used_ram += task.ram_req
        self.used_cores += task.cores_req

    def free(self, task: Task):
        """Освобождаем ресурсы после выполнения задачи."""
        self.used_memory -= task.memory_req
        self.used_ram -= task.ram_req
        self.used_cores -= task.cores_req

    def __repr__(self):
        return (f"<Server {self.server_id} usedMem={self.used_memory}/{self.total_memory} "
                f"usedRAM={self.used_ram}/{self.total_ram} usedCores={self.used_cores}/{self.total_cores}>")





def allocate_tasks_with_qubo(servers, tasks):

    N = len(tasks)
    M = len(servers)
    data_memory = []
    data_cores = []
    data_ram = []
    data_max_memory = []
    data_max_cores = []
    data_max_ram = []

    for el in tasks:
        data_memory.append(el.memory_req)
        data_cores.append(el.cores_req)
        data_ram.append(el.ram_req)
    
    for el in servers:
        data_max_memory.append(el.total_memory - el.used_memory)
        data_max_cores.append(el.total_cores - el.used_cores)
        data_max_ram.append(el.total_ram - el.used_ram)


    data = {
    "num_items": N,                  
    "memory" : data_memory,
    "cores" : data_cores,
    "ram" : data_ram,
    "max_memory" : data_max_memory,
    "max_cores" : data_max_cores,
    "max_ram" : data_max_ram
    }
    assigned = qubo_solver.give_ans(data, 3000) # (task, server)
    

    return assigned