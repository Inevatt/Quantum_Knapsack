import sys
import os
from ort import ort

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, "..")
sys.path.append(os.path.abspath(parent_dir))

####

from data_gen import generatedata
import solver



def main():
    data = generatedata(30)
    print("Цена: ", data["values"], "Вес:", data["weights"], "Макс вес: ", data["max_weight"])
    ans = solver.solve(data, 1000)
    ort(data)
    print("Ответ: ", ans[0], "Время: ", ans[1])
    return 0

main()