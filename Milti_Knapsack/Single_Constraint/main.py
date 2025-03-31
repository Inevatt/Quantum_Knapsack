import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, "..")
sys.path.append(os.path.abspath(parent_dir))

####

from data_gen import generatedata
import solver
from ort import ort


###1dрюкзак
###mdрюкзак
def main():
    data = generatedata(50, 8)
    print("Цена: ", data["values"], "Вес:", data["weights"], "Макс вес: ", data["knapsacks"])
    print("Правильный ответ: ", ort(data))
    ans = solver.solve(data, 2000)
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