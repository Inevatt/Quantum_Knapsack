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

def test_ortools_time(test_pairs):
    """
    Тестируем OR-Tools для увеличивающихся размеров задачи:
    - M (число серверов) идёт от 1 до max_servers с шагом step_servers,
    - N (число задач) идёт от 5 до max_tasks с шагом step_tasks.
    
    Если время решения > 5 минут, прерываем эксперимент, ставим 5 (минут) в график,
    возвращаем частичный результат.
    """



    results = []
    pairs = []
    
    # Для удобства пойдём двойным циклом по (M, N)
    for el in test_pairs:
        N = el[0]
        M = el[1]
        # Генерируем данные
        # N - количество задач, M - количество серверов
        data = generatedata(
            data_items_cnt=N, 
            data_knapsack_count=M
        )
        
        start = time.time()
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
        end = time.time()
        
        elapsed_minutes = end - start
        
        # Если превысили 5 минут, записываем 5 и прерываем эксперимент
        if elapsed_minutes > 300:
            results.append(300)
            pairs.append((N, M))
            print(f"Решение для M={M}, N={N} заняло > 5 минут. Останавливаемся.")
            # Важно: здесь мы прерываем цикл полностью
            return pairs, results
        else:
            results.append(int(elapsed_minutes))
            pairs.append((N, M))
    
    return pairs, results


def plot_ortools_results(pairs, results, out_filename="ortools_time.png"):
    """
    Строим график, где ось X - индекс пары (M,N), 
    а значение Y - время в минутах (не более 5).
    Сохраняем в PNG.
    """
    x_vals = range(len(pairs))
    y_vals = results
    
    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, y_vals, marker='o', label='OR-Tools time (min)')
    plt.xlabel("Index of (N,M) pair")
    plt.ylabel("Time in sec")
    plt.title("OR-Tools Scaling Test")
    plt.ylim(0, 320)
    plt.yticks(range(0, 311, 50))
    plt.grid(True)
    
    # Отметим на оси X сами пары (M, N)
    labels = [f"{p}" for p in pairs]
    plt.xticks(x_vals, labels, rotation=45)
    
    plt.tight_layout()
    plt.legend()
    plt.savefig("/home/andrey/Учёба/max_ortools_test6.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("График сохранен")


if __name__ == "__main__":
    # Пример запуска
    tasks =   [20, 40, 60, 80, 100,  120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 640, 680, 700, 720, 740, 760, 780, 800,
                840, 880, 920, 960, 1000, 1040, 1080, 1120, 1160, 1200, 1240, 1280, 1320, 1360, 1400]
    
    servers = [1,  2,  3,  4,   5,   6,   7,   8,   9,   10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29,  30,  32,  34,  35,  36,  37,  38,  39,  40,
                 42,  44,  46,  48,  50,   52,   54,   56,   58,   60,   62,  64,   66,   68,   70]
    
    # Формируем пары посредством zip
    test_pairs = list(zip(tasks, servers))
    pairs, results = test_ortools_time(test_pairs)
    plot_ortools_results(pairs, results)