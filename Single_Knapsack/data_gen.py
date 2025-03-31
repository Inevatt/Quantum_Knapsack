from random import randint

def generatedata(data_items_cnt, value_from = None, value_to = None, 
                 weight_from = None, weight_to = None, knapsack_full = None):
    
    if ((value_from is None) and (value_to is None) and
         (weight_from is None) and (weight_to is None)):
        value_from = 1
        value_to = 30
        weight_from = 1
        weight_to = 100
        cores_from = 1
        cores_to = 12

    elif (((value_from is None) + (value_to is None)) == 1):
        raise ValueError("Если введён один параметр у границ значений, то нужно ввести и второй")
    elif (((weight_from is None) + (weight_to is None)) == 1):
        raise ValueError("Если введён один параметр у границ значений, то нужно ввести и второй")
    
    data_values = [int(randint(value_from, value_to)) for _ in range(data_items_cnt)]
    data_weights = [int(randint(weight_from, weight_to)) for _ in range(data_items_cnt)]

    if (knapsack_full == None) :
        sm = sum(data_weights)
        knapsack_full = sm - randint(0, sm)

    data = {
    "num_items": data_items_cnt,                 
    "values": data_values,  
    "weights": data_weights,    
    "max_weight": knapsack_full,                
    "first_lambda": 10,
    "second_lambda": 10
    }
    return data