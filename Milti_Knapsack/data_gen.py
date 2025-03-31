from random import randint
import numpy as np

def generatedata(
        data_items_cnt, 
        data_knapsack_count = 1,
        value_from = None,
        value_to = None, 
        weight_from = None,
        weight_to = None,
        cores_from = None,
        cores_to = None,
        ram_from = None,
        ram_to = None, 
        data_cores = None,
        data_ram = None, 
        data_knapsacks = None,
        data_max_cores = None,
        data_max_ram = None):
    




    
    if ((value_from is None) and (value_to is None) and
         (weight_from is None) and (weight_to is None) and 
         (cores_from is None) and (cores_to is None) and 
         (ram_from is None) and (ram_to is None)):
        value_from = 1
        value_to = 30
        weight_from = 100
        weight_to = 200
        cores_from = 1
        cores_to = 10
        ram_from = 1
        ram_to = 40

    elif (((value_from is None) + (value_to is None)) == 1):
        raise ValueError("Если введён один параметр у границ значений, то нужно ввести и второй")
    elif (((weight_from is None) + (weight_to is None)) == 1):
        raise ValueError("Если введён один параметр у границ значений, то нужно ввести и второй")
    
    data_values = [int(randint(value_from, value_to)) for _ in range(data_items_cnt)]
    data_weights = [int(randint(weight_from, weight_to)) for _ in range(data_items_cnt)]

    # Потребление ядер (p_i)
    data_cores = [randint(cores_from, cores_to) for _ in range(data_items_cnt)]
    # Потребление ОЗУ (op_i)
    data_ram = [randint(ram_from, ram_to) for _ in range(data_items_cnt)]


    if data_knapsacks is None:
        data_knapsacks = []
        sum_memory = sum(data_weights)
        for _ in range(data_knapsack_count):
            data_knapsacks.append(randint(int(sum_memory//len(data_weights)), int(sum_memory//len(data_weights))*4))

    if data_max_cores is None:
        data_max_cores = []
        sum_cores = sum(data_cores)
        for _ in range(data_knapsack_count):
            data_max_cores.append(randint(int(sum_cores//len(data_cores)), int(sum_cores//len(data_cores))*4))

    if data_max_ram is None:
        data_max_ram = []
        sum_ram = sum(data_ram)
        for _ in range(data_knapsack_count):
            data_max_ram.append(randint(int(sum_ram//len(data_ram)), int(sum_ram // len(data_ram))*4))


    data = {
    "num_items": data_items_cnt,                 
    "values": data_values,  
    "weights": data_weights,
    "memory" : data_weights,
    "cores" : data_cores,
    "ram" : data_ram,   
    "knapsacks": data_knapsacks,
    "max_memory" : data_knapsacks,
    "max_cores" : data_max_cores,
    "max_ram" : data_max_ram,                
    "first_lambda": 10000,
    "second_lambda": 10000,
    "slack" : (np.ceil(np.log2(data_knapsacks)+1)).astype(int)
    }
    return data