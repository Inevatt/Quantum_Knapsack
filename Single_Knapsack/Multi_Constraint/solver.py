from dimod import BinaryQuadraticModel 
from dwave.samplers import SimulatedAnnealingSampler
from to_qubo_strong2 import build_qubo2
import time

def solve(data, num_reads):
    
    Q = build_qubo2(data)
    
    bqm = BinaryQuadraticModel.from_qubo(Q)
    
    seconds_before = time.time()
    
    response = SimulatedAnnealingSampler().sample(bqm, num_reads=num_reads)
    
    seconds_after = time.time()

    offset = data["max_weight"] ** 2 * data["first_lambda"]

    answer = -(response.first.energy + offset)
    
    total_time = seconds_after - seconds_before
    
    return answer, total_time