"""Solves a multiple knapsack problem using the CP-SAT solver."""
from ortools.sat.python import cp_model


def ort(data_g):
    data = {}
    data["weights"] = data_g["weights"]
    data["values"] = data_g["values"]
    assert len(data["weights"]) == len(data["values"])
    num_items = len(data["weights"])
    all_items = range(num_items)

    data["bin_capacities"] = data_g["knapsacks"]
    num_bins = len(data["bin_capacities"])
    all_bins = range(num_bins)

    model = cp_model.CpModel()

    # Variables.
    # x[i, b] = 1 if item i is packed in bin b.
    x = {}
    for i in all_items:
        for b in all_bins:
            x[i, b] = model.new_bool_var(f"x_{i}_{b}")

    # Constraints.
    # Each item is assigned to at most one bin.
    for i in all_items:
        model.add_at_most_one(x[i, b] for b in all_bins)

    # The amount packed in each bin cannot exceed its capacity.
    for b in all_bins:
        model.add(
            sum(x[i, b] * data["weights"][i] for i in all_items)
            <= data["bin_capacities"][b]
        )

    # Objective.
    # maximize total value of packed items.
    objective = []
    for i in all_items:
        for b in all_bins:
            objective.append(cp_model.LinearExpr.term(x[i, b], data["values"][i]))
    model.maximize(cp_model.LinearExpr.sum(objective))

    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if status == cp_model.OPTIMAL:
        return solver.objective_value
    else:
        print("The problem does not have an optimal solution.")

