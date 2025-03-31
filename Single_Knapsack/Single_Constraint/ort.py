from ortools.algorithms.python import knapsack_solver


def ort(data):
    # Create the solver.
    solver = knapsack_solver.KnapsackSolver(
        knapsack_solver.SolverType.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
        "KnapsackExample",
    )

    values = data["values"]
    weights = [
        # fmt: off
      data["weights"],
        # fmt: on
    ]
    capacities = [data["max_weight"]]

    solver.init(values, weights, capacities)
    computed_value = solver.solve()

    print("Правильный ответ", computed_value)
    return 0