import sys
import os
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, "..")
sys.path.append(os.path.abspath(parent_dir))

####

from data_gen import generatedata
import qubo_solver
from ort import solve_task_selection




def main():
    data = generatedata(5, 1)

    correct = solve_task_selection(
    data["num_items"], 
    len(data["max_cores"]), 
    data["memory"], 
    data["ram"], 
    data["cores"], 
    data["max_cores"],  # A: макс. ядра серверов (P_i)
    data["max_memory"],  # B: макс. память (W_i)
    data["max_ram"]      # C: макс. RAM (R_i)
)

    print("память:", data["weights"], '\n', "Ядра: ", data["cores"], '\n', "Опер: ",data["ram"])
    print("Макс вес: ", data["max_memory"], '\n', "Макс ядра: ", data["max_cores"], '\n', "Макс опер: ", data["max_ram"])
    good, tm = qubo_solver.give_ans(data, 3000)
    if (good):
        print("ОтветМОЙ:", good, "Время:", tm)
    else:
        print("Нет допустимых решений")
    return 0
main()