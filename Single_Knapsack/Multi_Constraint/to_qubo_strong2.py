import numpy as np
def build_qubo2(data):
    
    count_of_elements = data["num_items"]
    
    number_of_slack_bits = int(np.round(np.log2(max(data["weights"])+1)))
    
    total_count_of_bits = count_of_elements + number_of_slack_bits

    data_values_array = np.array(data["values"] + [0 for _ in range(number_of_slack_bits)])
        
    data_weights_array = np.array(data["weights"] + [2**k for k in range(number_of_slack_bits)])
    
    Q = np.zeros((total_count_of_bits, total_count_of_bits))
    
    for i in range(total_count_of_bits):
        Q[i][i] = -data_values_array[i] - data["first_lambda"] * data_weights_array[i] * (2 * data["max_weight"] - data_weights_array[i])
        for j in range(i + 1, total_count_of_bits):
            Q[i][j] = 2 * data["first_lambda"] * data_weights_array[i] * data_weights_array[j]
    
    return Q