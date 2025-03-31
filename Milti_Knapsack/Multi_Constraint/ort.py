from ortools.linear_solver import pywraplp

def solve_task_selection(N, M, alpha, beta, gamma, A, B, C):
    """
    Решает задачу распределения задач по серверам с использованием OR-Tools.
    Возвращает максимальное количество размещенных задач.
    """
    # Создание решателя
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    # Создание бинарных переменных x[i][j]
    x = {}
    for i in range(N):
        for j in range(M):
            x[i, j] = solver.BoolVar(f'x_{i}_{j}')
    
    # Целевая функция: максимизация количества размещенных задач
    objective = solver.Objective()
    for i in range(N):
        for j in range(M):
            objective.SetCoefficient(x[i, j], 1)
    objective.SetMaximization()
    
    # Ограничение: каждая задача назначается не более чем на один сервер
    for i in range(N):
        constraint = solver.Constraint(0, 1)  # sum(x[i][j]) <= 1
        for j in range(M):
            constraint.SetCoefficient(x[i, j], 1)
    
    # Ограничения ресурсов серверов
    for j in range(M):
        # Ограничение по ядрам (gamma)
        constraint_cores = solver.Constraint(-solver.infinity(), A[j])
        for i in range(N):
            constraint_cores.SetCoefficient(x[i, j], gamma[i])
        
        # Ограничение по памяти (alpha)
        constraint_disk = solver.Constraint(-solver.infinity(), B[j])
        for i in range(N):
            constraint_disk.SetCoefficient(x[i, j], alpha[i])
        
        # Ограничение по RAM (beta)
        constraint_ram = solver.Constraint(-solver.infinity(), C[j])
        for i in range(N):
            constraint_ram.SetCoefficient(x[i, j], beta[i])
    
    # Решение задачи
    status = solver.Solve()
    
    if status in [solver.OPTIMAL, solver.FEASIBLE]:
        return int(objective.Value())
    else:
        return 0