import numpy as np
from itertools import combinations


def build_qubo1(data):
    data_max_memory_list = np.array(data["max_memory"])
    data_max_ram_list = np.array(data["max_ram"])
    data_max_cores_list = np.array(data["max_cores"])

    num_knapsacks = len(data_max_memory_list)
    
    num_items = data["num_items"]

    # создаём для удобства двумерный массив
    # для более широкой постановки можно изменить реализацию
    # на произвольные значения для каждого из рюкзаков
    data_memory_array = data["memory"]
    data_ram_array = data["ram"]
    data_cores_array = data["cores"]
    
    # определяем соответствующие коэффициенты
    # koeff_1 = 2 * np.max(np.concatenate(data_memory_array).ravel()) + 1
    # koeff_2 = 2 * np.max(np.concatenate(data_ram_array).ravel()) + 1
    # koeff_3 = 2 * np.max(np.concatenate(data_cores_array).ravel()) + 1
    # alpha = max(koeff_1, koeff_2, koeff_3)
    cn = len(data["memory"])
    koeff_1 = 10*max(data_memory_array)*cn
    koeff_2 = 10*max(data_ram_array)*cn
    koeff_3 = 10*max(data_cores_array)*cn
    alpha = 2*koeff_1
    goal_kef = 10


    # количество дополнительных битов для каждого рюкзака по отдельности
    num_slack_bits = (np.floor(np.log2(np.array(data["max_memory"]))) + 1
                    + np.floor(np.log2(np.array(data["max_cores"]))) + 1
                    + np.floor(np.log2(np.array(data["max_ram"]))) + 1).astype(int)
    
    num_slack_bits_array_memory = (np.floor(np.log2(np.array(data["max_memory"]))) + 1).astype(int)
    num_slack_bits_array_ram = (np.floor(np.log2(np.array(data["max_ram"]))) + 1).astype(int)
    num_slack_bits_array_cores = (np.floor(np.log2(np.array(data["max_cores"]))) + 1).astype(int)

    
    # общее количество переменных
    num_qubits = (num_items * num_knapsacks + num_slack_bits.sum()).astype(int)

    Q = np.zeros((num_qubits, num_qubits))

    # заполнение диагональных элементов
    for i in range(num_knapsacks):
        base_i = sum(num_items + num_slack_bits[k] for k in range(i))
        # в терминах x_ij
        for j in range(num_items):
            # вычисление индекса на диагонали
            index = base_i + j
            # заполняем диагональ (максимизация используемых ресурсов)
            Q[index][index] += koeff_1 * data_memory_array[j] ** 2 - 2 * koeff_1 * data_max_memory_list[i] * data_memory_array[j]
            Q[index][index] += koeff_2 * data_ram_array[j] ** 2 - 2 * koeff_2 * data_max_ram_list[i] * data_ram_array[j]
            Q[index][index] += koeff_3 * data_cores_array[j] ** 2 - 2 * koeff_3 * data_max_cores_list[i] * data_cores_array[j]
            Q[index][index] -=goal_kef

        # в терминах a_ib -- заполнение диагонали (огр. диска)
        for b in range(num_slack_bits_array_memory[i]):
            index = base_i + num_items + b
            Q[index][index] += koeff_1 * 2 ** (2 * b) - 2 * koeff_1 * data_max_memory_list[i] * 2 ** b
            
        # в терминах b_ib -- заполнение диагонали (огр. оперативной памяти)
        for b in range(num_slack_bits_array_ram[i]):
            index = base_i + num_items + num_slack_bits_array_memory[i] + b
            Q[index][index] += koeff_2 * 2 ** (2 * b) - 2 * koeff_2 * data_max_ram_list[i] * 2 ** b
            
        # в терминах c_ib -- заполнение диагонали (огр. ядер)
        for b in range(num_slack_bits_array_cores[i]):
            index = base_i + num_items + num_slack_bits_array_memory[i] + num_slack_bits_array_ram[i] + b
            Q[index][index] += koeff_3 * 2 ** (2 * b) - 2 * koeff_3 * data_max_cores_list[i] * 2 ** b

    # создаём всевозможные пары предметов
    knapsack_ind_pairs = list(combinations(range(num_knapsacks), 2))
    item_ind_pairs = list(combinations(range(num_items), 2))

    slack_ind_pairs_memory = []
    for i in range(num_knapsacks):
        slack_ind_pairs_memory.append(list(combinations(range(num_slack_bits_array_memory[i]), 2)))

    slack_ind_pairs_ram = []
    for i in range(num_knapsacks):
        slack_ind_pairs_ram.append(list(combinations(range(num_slack_bits_array_ram[i]), 2)))

    slack_ind_pairs_cores = []
    for i in range(num_knapsacks):
        slack_ind_pairs_cores.append(list(combinations(range(num_slack_bits_array_cores[i]), 2)))

    # пенальти на вне диагональные элементы: нельзя быть в нескольких рюкзаках одновременно
    for j in range(num_items):
        for pair in knapsack_ind_pairs:
            index1 = pair[0] * num_items + num_slack_bits[:pair[0]].sum() + j
            index2 = pair[1] * num_items + num_slack_bits[:pair[1]].sum() + j
            Q[index1][index2] += alpha
            Q[index2][index1] += alpha

    # пенальти на все ограничения для xx
    for i in range(num_knapsacks):
        for pair in item_ind_pairs:
            index1 = i * num_items + num_slack_bits[:i].sum() + pair[0]
            index2 = i * num_items + num_slack_bits[:i].sum() + pair[1]
            Q[index1][index2] += koeff_1 * data_memory_array[pair[0]] * data_memory_array[pair[1]]
            Q[index2][index1] += koeff_1 * data_memory_array[pair[0]] * data_memory_array[pair[1]]

            Q[index1][index2] += koeff_2 * data_ram_array[pair[0]] * data_ram_array[pair[1]]
            Q[index2][index1] += koeff_2 * data_ram_array[pair[0]] * data_ram_array[pair[1]]

            Q[index1][index2] += koeff_3 * data_cores_array[pair[0]] * data_cores_array[pair[1]]
            Q[index2][index1] += koeff_3 * data_cores_array[pair[0]] * data_cores_array[pair[1]]

    # пенальти на ограничения для yy
    for i in range(num_knapsacks):
        base_i = sum(num_items + num_slack_bits[k] for k in range(i))
        # вместительность диска
        for pair in slack_ind_pairs_memory[i]:
            index1 = base_i + num_items + pair[0]
            index2 = base_i + num_items + pair[1]
            Q[index1][index2] += koeff_1 * 2 ** (pair[0] + pair[1])
            Q[index2][index1] += koeff_1 * 2 ** (pair[0] + pair[1])
        
        # вместительность оперативной памяти
        for pair in slack_ind_pairs_ram[i]:
            index1 = base_i + num_items + num_slack_bits_array_memory[i] + pair[0]
            index2 = base_i + num_items + num_slack_bits_array_memory[i] + pair[1]
            Q[index1][index2] += koeff_2 * 2 ** (pair[0] + pair[1])
            Q[index2][index1] += koeff_2 * 2 ** (pair[0] + pair[1])
        
        # вместительность по количеству ядер
        for pair in slack_ind_pairs_cores[i]:
            index1 = base_i + num_items + num_slack_bits_array_memory[i] + num_slack_bits_array_ram[i] + pair[0]
            index2 = base_i + num_items + num_slack_bits_array_memory[i] + num_slack_bits_array_ram[i] + pair[1]
            Q[index1][index2] += koeff_3 * 2 ** (pair[0] + pair[1])
            Q[index2][index1] += koeff_3 * 2 ** (pair[0] + pair[1])

    # пенальти на вместительность на xy
    for i in range(num_knapsacks):
        base_i = sum(num_items + num_slack_bits[k] for k in range(i))
        for j in range(num_items):   

            # вместительность по диску
            for b in range(num_slack_bits_array_memory[i]):
                index1 = i * num_items + num_slack_bits[:i].sum() + j
                index2 = base_i + num_items + b
                Q[index1][index2] += koeff_1 * data_memory_array[j] * 2 ** b
                Q[index2][index1] += koeff_1 * data_memory_array[j] * 2 ** b
            
            # вместительность по оперативной памяти
            for b in range(num_slack_bits_array_ram[i]):
                index1 = i * num_items + num_slack_bits[:i].sum() + j
                index2 = base_i + num_items + num_slack_bits_array_memory[i] + b
                Q[index1][index2] += koeff_2 * data_ram_array[j] * 2 ** b
                Q[index2][index1] += koeff_2 * data_ram_array[j] * 2 ** b
            
            # вместительность по количеству ядер
            for b in range(num_slack_bits_array_cores[i]):
                index1 = i * num_items + num_slack_bits[:i].sum() + j
                index2 = base_i + num_items + num_slack_bits_array_memory[i] + num_slack_bits_array_ram[i] + b
                Q[index1][index2] += koeff_3 * data_cores_array[j] * 2 ** b
                Q[index2][index1] += koeff_3 * data_cores_array[j] * 2 ** b

    offset = koeff_1 * (data_max_memory_list ** 2).sum()
    offset += koeff_2 * (data_max_ram_list ** 2).sum()
    offset += koeff_3 * (data_max_cores_list ** 2).sum()

    return Q, offset

