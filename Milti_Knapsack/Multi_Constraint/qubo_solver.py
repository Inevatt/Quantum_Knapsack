from dimod import BinaryQuadraticModel 
from dwave.samplers import SimulatedAnnealingSampler
from build_qubo import build_qubo1
import time
import numpy as np
import signal

def give_ans(data, num_reads, test = 0):
    if test == 0:
        ans, tm = solve(data, num_reads=num_reads)
    else:
        ans, tm = solve_test(data, num_reads=num_reads)
        if ans == None:
            return 1

    samples = sorted(ans.data(['sample', 'energy']), key=lambda x: x.energy)
    samples = samples[:5]
    good = 0
    for sample in samples:
        total = check_samples(data, sample.sample)
        if (total != 0):
            if (total > good):
                good = total
    return good, tm


def solve(data, num_reads, beta_range = None):
    
    Q1, offset1 = build_qubo1(data)


    
    bqm1 = BinaryQuadraticModel.from_qubo(Q1, offset=offset1)

    
    seconds_before = time.time()
    if (beta_range is None):
        response1 = SimulatedAnnealingSampler().sample(bqm1, num_reads=num_reads, num_sweeps = 5000)
    else:
        response1 = SimulatedAnnealingSampler().sample(bqm1, num_reads=num_reads, beta_range=beta_range)
                                                   

    seconds_after = time.time()
    
    
    total_time = seconds_after - seconds_before
    
    return response1, total_time


def check_samples(data, sample):
    total = 0
    slack = (np.floor(np.log2(np.array(data["max_memory"]))) + 1
                    + np.floor(np.log2(np.array(data["max_cores"]))) + 1
                    + np.floor(np.log2(np.array(data["max_ram"]))) + 1).astype(int)
    for i in range(len(data["knapsacks"])):
        max_i_m = data["knapsacks"][i]
        max_i_r = data["max_ram"][i]
        max_i_c = data["max_cores"][i]
        value_m = 0
        value_r = 0
        value_c = 0
        for j in range(data["num_items"]):
            ind = i*data["num_items"] + slack[:i].sum() + j
            if (sample[ind]):
                value_m+=data["weights"][j]
                value_r+=data["ram"][j]
                value_c+=data["cores"][j]
        if (value_m > max_i_m):
            return 0
        if (value_r > max_i_r):
            return 0
        if (value_c > max_i_c):
            return 0
    
    for j in range(data["num_items"]):
        count = 0
        for i in range(len(data["knapsacks"])):
            ind = i*data["num_items"] + slack[:i].sum() + j
            if (sample[ind]):
                count += 1
                total+=1
        if (count > 1):
            return 0
    return total




############
def timeout_handler(signum, frame):
    # Вместо того, чтобы выбрасывать исключение, можно просто возвращать None
    raise TimeoutError  # Мы всё же вызываем исключение, но ниже перехватываем его

def call_sample(bqm1, num_reads):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(360)  # 360 секунд = 6 минут
    try:
        result = SimulatedAnnealingSampler().sample(bqm1, num_reads=num_reads)
        return result
    except TimeoutError:
        # Вместо ошибки возвращаем значение по умолчанию
        return None
    finally:
        signal.alarm(0)  # Отключаем таймер

def solve_test(data, num_reads):
    Q1, offset1 = build_qubo1(data)
    bqm1 = BinaryQuadraticModel.from_qubo(Q1, offset=offset1)
    
    seconds_before = time.time()
    response1 = call_sample(bqm1, num_reads)
    seconds_after = time.time()
    
    total_time = seconds_after - seconds_before
    # Можно проверить, что если response1 is None, то обработать это как timeout
    return response1, total_time
