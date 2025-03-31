import sys
import os
import numpy as np
from ort import ort

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, "..")
sys.path.append(os.path.abspath(parent_dir))

####

from data_gen import generatedata
import solver



def main():
    data_weights = [150, 138, 123, 105, 182, 177, 169, 162, 186, 148, 175, 191, 110, 142, 105, 110, 122, 188, 135, 130]
    data_knapsacks = [1463, 90, 944, 1218, 709]
    data_values = [6, 27, 30, 23, 11, 10, 28, 2, 5, 8, 1, 28, 11, 26, 28, 21, 9, 7, 28, 10]
    data = {
    "num_items": 20,                 
    "values": data_values,  
    "weights": data_weights,    
    "knapsacks": data_knapsacks,                
    "first_lambda": 2,
    "second_lambda": 2,
    "slack" : (np.floor(np.log2(data_knapsacks))+1).astype(int)
    }
    print("Цена: ", data["values"], "Вес:", data["weights"], "Макс вес: ", data["knapsacks"])
    ans = solver.solve(data, 10000)
    samples = sorted(ans[0].data(['sample', 'energy']), key=lambda x: x.energy)
    samples = samples[:100]
    good = []
    for sample in samples:
        total = solver.check_samples(data, sample.sample)
        if (total != 0):
            good.append(total)

    print("energy, ", ans[0].first.energy)
    if (good):
        print("ОтветМОЙ:", max(good))
    else:
        print("Нет допустимых решений")
    return 0

main()