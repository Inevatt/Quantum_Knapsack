import os
import sys
# Определяем путь к директории, которая находится на один уровень выше
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '../'))
# Добавляем эту директорию в sys.path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)



from dimod import BinaryQuadraticModel 
from dwave.samplers import SimulatedAnnealingSampler
from build_qubo import build_qubo1
import time

def solve(data, num_reads):
    
    Q1, offset1 = build_qubo1(data)
    
    bqm1 = BinaryQuadraticModel.from_qubo(Q1, offset=offset1)
    
    seconds_before = time.time()
    
    response1 = SimulatedAnnealingSampler().sample(bqm1, num_reads=num_reads)
    
    seconds_after = time.time()
    
    sample1 = response1.first.energy
    
    
    total_value1 = -sample1
    
    total_time = seconds_after - seconds_before
    
    return response1, total_time


def check_samples(data, sample):
    total = 0
    for i in range(len(data["knapsacks"])):
        max_i = data["knapsacks"][i]
        value = 0
        for j in range(data["num_items"]):
            ind = i*data["num_items"] + data["slack"][:i].sum() + j
            if (sample[ind]):
                value+=data["weights"][j]
        if (value > max_i):
            return 0
    
    for j in range(data["num_items"]):
        count = 0
        for i in range(len(data["knapsacks"])):
            ind = i*data["num_items"] + data["slack"][:i].sum() + j
            if (sample[ind]):
                count += 1
                total+=data["values"][j]
        if (count > 1):
            return 0
    return total

