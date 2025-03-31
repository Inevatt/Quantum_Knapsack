from dimod import BinaryQuadraticModel 
from dwave.samplers import SimulatedAnnealingSampler
from build_qubo import build_qubo1
import time
import numpy as np

def give_ans(data, num_reads):

    response, tm = solve(data, num_reads=num_reads)
    sample_first = response.first

    if (check_samples(data, sample_first.sample)):
        assign = make_assign(data, sample_first.sample)
        return assign
    else:
        samples = sorted(response.data(['sample', 'energy']), key=lambda x: x.energy)
        samples = samples[:5]
        for sample in samples:
            if(check_samples(data, sample.sample)):
                assign = make_assign(data, sample.sample)
                return assign
        return -1


def solve(data, num_reads = 2000, beta_range = None):
    
    Q1, offset1 = build_qubo1(data)


    
    bqm1 = BinaryQuadraticModel.from_qubo(Q1, offset=offset1)

    
    seconds_before = time.time()
    if (beta_range is not None):
        response1 = SimulatedAnnealingSampler().sample(bqm1, num_reads=num_reads, beta_range=beta_range)
    else:
        response1 = SimulatedAnnealingSampler().sample(bqm1, num_reads=num_reads)
                                                   

    seconds_after = time.time()
    
    
    total_time = seconds_after - seconds_before
    
    return response1, total_time


def check_samples(data, sample):
    total = 0
    slack = (np.floor(np.log2(np.array(data["max_memory"]))) + 1
                    + np.floor(np.log2(np.array(data["max_cores"]))) + 1
                    + np.floor(np.log2(np.array(data["max_ram"]))) + 1).astype(int)
    for i in range(len(data["max_memory"])):
        max_i_m = data["max_memory"][i]
        max_i_r = data["max_ram"][i]
        max_i_c = data["max_cores"][i]
        value_m = 0
        value_r = 0
        value_c = 0
        for j in range(data["num_items"]):
            ind = i*data["num_items"] + slack[:i].sum() + j
            if (sample[ind]):
                value_m+=data["memory"][j]
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
        for i in range(len(data["max_memory"])):
            ind = i*data["num_items"] + slack[:i].sum() + j
            if (sample[ind]):
                count += 1
                total+=1
        if (count > 1):
            return 0
    return total


def make_assign(data, sample):
    slack = (np.floor(np.log2(np.array(data["max_memory"]))) + 1
                    + np.floor(np.log2(np.array(data["max_cores"]))) + 1
                    + np.floor(np.log2(np.array(data["max_ram"]))) + 1).astype(int)

    assign = []
    for j in range(data["num_items"]):
        for i in range(len(data["max_memory"])):
            ind = i*data["num_items"] + slack[:i].sum() + j
            if (sample[ind]):
                assign.append((j, i))
    return assign