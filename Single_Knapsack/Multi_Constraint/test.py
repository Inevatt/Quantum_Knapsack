import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, "..")
sys.path.append(os.path.abspath(parent_dir))

import solver



def main():
    data = {
    "num_items": 10,                 
    "values": [65, 58, 59, 96, 9, 85, 74, 34, 16, 72],  
    "weights": [79, 23, 30, 88, 96, 48, 17, 69, 2, 74],    
    "max_weight": 310,                
    "first_lambda": 100000,
    "second_lambda": 10000
    }
    print("Цена: ", data["values"], "Вес:", data["weights"], "Макс вес: ", data["max_weight"])
    ans = solver.solve(data, 500)
    print("Ответ: ", ans[0], "Время: ", ans[1])
    return 0

main()