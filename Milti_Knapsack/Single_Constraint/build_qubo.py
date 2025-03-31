import numpy as np
from itertools import combinations

def build_qubo1(data):
        data_max_weights_list = np.array(data["knapsacks"])
    
        num_knapsacks = len(data_max_weights_list)
        
        num_items = data["num_items"]
    
        data_weights_array = data["weights"]
        data_values_array = data["values"]
    
        # определяем соответствующие коэффициенты
        betta = 10000
        alpha = 10000
        gamma = 1000
    
        # количество дополнительных битов для каждого рюкзака по отдельности
        num_slack_bits = (np.ceil(np.log2(data_max_weights_list) + 1)).astype(int)
        
        # общее количество битов
        num_qubits = (num_items * num_knapsacks + num_slack_bits.sum()).astype(int)

        Q = np.zeros((num_qubits, num_qubits))

        # заполнение диагональных элементов
        for i in range(num_knapsacks):
            base_i = sum(num_items + num_slack_bits[k] for k in range(i))
            # в терминах x_ij
            for j in range(num_items):
                # вычисление индекса на диагонали
                index = base_i + j
                # заполняем диагональ
                Q[index][index] = betta * data_weights_array[j] ** 2 - 2 * betta * data_max_weights_list[i] \
                * data_weights_array[j] - gamma * data_values_array[j]

            # в терминах y_ib
            for b in range(num_slack_bits[i]):
                index = base_i + num_items + b
                Q[index][index] = betta * 2 ** (2 * b) - 2 * betta * data_max_weights_list[i] * 2 ** b

        # создаём всевозможные пары предметов
        knapsack_ind_pairs = list(combinations(range(num_knapsacks), 2))
        item_ind_pairs = list(combinations(range(num_items), 2))

        slack_ind_pairs = []
        for i in range(num_knapsacks):
            slack_ind_pairs.append(list(combinations(range(num_slack_bits[i]), 2)))


        # пенальти на вне диагональные элементы: нельзя быть в нескольких рюкзаках одновременно
        for j in range(num_items):
            for pair in knapsack_ind_pairs:
                index1 = pair[0] * num_items + num_slack_bits[:pair[0]].sum() + j
                index2 = pair[1] * num_items + num_slack_bits[:pair[1]].sum() + j
                Q[index1][index2] = alpha
                Q[index2][index1] = alpha

        # пенальти на вместительность для xx
        for i in range(num_knapsacks):
            for pair in item_ind_pairs:
                index1 = i * num_items + num_slack_bits[:i].sum() + pair[0]
                index2 = i * num_items + num_slack_bits[:i].sum() + pair[1]
                Q[index1][index2] = Q[index2][index1] = betta * data_weights_array[pair[0]] * data_weights_array[pair[1]]

        # пенальти на вместительность для yy
        for i in range(num_knapsacks):
            base_i = sum(num_items + num_slack_bits[k] for k in range(i))
            for pair in slack_ind_pairs[i]:
                index1 = base_i + num_items + pair[0]
                index2 = base_i + num_items + pair[1]
                Q[index1][index2] = Q[index2][index1] = betta * 2 ** (pair[0] + pair[1])

        # пенальти на вместительность на xy
        for i in range(num_knapsacks):
            base_i = sum(num_items + num_slack_bits[k] for k in range(i))
            for j in range(num_items):
                for b in range(num_slack_bits[i]):
                    index1 = i * num_items + num_slack_bits[:i].sum() + j
                    index2 = base_i + num_items + b
                    Q[index1][index2] = Q[index2][index1] = betta * data_weights_array[j] * 2 ** b

        offset = betta * (data_max_weights_list ** 2).sum()

        return Q, offset


