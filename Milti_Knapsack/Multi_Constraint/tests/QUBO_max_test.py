import sys
import os
import time
import matplotlib.pyplot as plt

# --- Добавляем путь к верхним директориям, если нужно ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '../'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

parent_dir_2 = os.path.abspath(os.path.join(current_dir, '../../'))
if parent_dir_2 not in sys.path:
    sys.path.insert(0, parent_dir_2)

# --- Импорт вашего кода ---
from data_gen import generatedata
from ort import solve_task_selection
import qubo_solver


def test_QUBO_time(data_list, num_reads):
    results = []

    accur = 0
    n = 0
    
    # Для удобства пойдём двойным циклом по (M, N)
    for i in range(len(data_list)):
        data = data_list[i]
        # Генерируем данные
        # N - количество задач, M - количество серверов
        

        ans_ort = solve_task_selection(
            data["num_items"],  # N
            len(data["max_cores"]),  # M
            data["memory"], 
            data["ram"], 
            data["cores"], 
            data["max_cores"],   # макс. ядра серверов (P_i)
            data["max_memory"],  # макс. память (W_i)
            data["max_ram"]      # макс. RAM (R_i)
        )
        start = time.time()
        good = qubo_solver.give_ans(data, num_reads, 1)[0]
        end = time.time()
        
        elapsed_minutes = end - start
        
        # Если превысили 5 минут, записываем 5 и прерываем эксперимент
        if elapsed_minutes > 300:
            j = i
            while j < len(data_list):
                results.append(300)
                j+=1
            print("Решение заняло > 5 минут. Останавливаемся.")
            # Важно: здесь мы прерываем цикл полностью
            if (accur == 0 or ans_ort == 0):
                return results, 100
            else:
                return results, accur/n
        else:
            accur+=(1 - abs(good - ans_ort)/ans_ort)*100
            n+=1
            results.append(int(elapsed_minutes))
    
    return results, accur/n


def plot_qubo_time_all(pairs, results_dict, out_filename="qubo_time.png"):
    """
    Строит график времени (секунды) для разных значений num_reads.
    results_dict предполагается словарём:
        {
          num_reads_1: [t_1, t_2, ...],
          num_reads_2: [t_1, t_2, ...],
          ...
        }
    где каждое [t_1, t_2, ...] соответствует одному и тому же `pairs`.
    """
    x_vals = range(len(pairs))
    
    plt.figure(figsize=(10,6))
    for num_reads, times_list in results_dict.items():
        plt.plot(x_vals, times_list, marker='o', label=f'num_reads={num_reads}')
    
    # Подписи осей
    plt.xlabel("Index of (N,M) pair")
    plt.ylabel("Time sec")
    plt.title("QUBO Time Comparison")
    plt.ylim(0, 320)
    plt.yticks(range(0, 311, 50))
    plt.grid(True)
    
    # Если хотите подписать ось X самими парами:
    labels = [f"{p}" for p in pairs]
    plt.xticks(x_vals, labels, rotation=45)
    
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"График времени сохранен в {out_filename}")





def plot_qubo_accur(num_reads_list, accur_list, out_filename="qubo_accuracy.png"):
    plt.figure(figsize=(8,5))
    plt.plot(num_reads_list, accur_list, marker='o', label='Mean Accuracy')
    plt.xlabel("num_reads")
    plt.ylabel("Mean Accuracy")
    plt.title("QUBO Accuracy vs num_reads")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"График точности сохранен в {out_filename}")

if __name__ == "__main__":
    # Пример набора пар (N, M)
    tasks =   [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260]
    servers = [1,  2,  3,  4,  5,   6,   7,   8,   9,   10,  11,  12,  13]

    data_list = []
    test_pairs = list(zip(tasks, servers))
    for i in test_pairs:
        dat = generatedata(i[0], i[1])
        data_list.append(dat)
    
    # Список интересующих нас num_reads
    num_reads_list = [1000, 2000, 3000]
    

    results_dict = {}
    accur_list = []
    
    for nr in num_reads_list:
        times, accur = test_QUBO_time(data_list, nr)
        results_dict[nr] = times
        accur_list.append(accur)
    
    # 1) Строим график времени (3 линии на одном, по количеству num_reads)
    plot_qubo_time_all(test_pairs, results_dict, out_filename="qubo_time.png")
    
    # 2) Строим график точности (по оси X — num_reads, по оси Y — средняя точность)
    plot_qubo_accur(num_reads_list, accur_list, out_filename="qubo_accuracy.png")