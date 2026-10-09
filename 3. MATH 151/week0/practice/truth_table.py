from itertools import product


def truth_table(formula, variables):
    """
    formula: a function (dict -> bool)
    variables: list of variable names
    """
    print(" | ".join(variables) + " | result")
    print("-" * (4 * (len(variables) + 1)))
    for assignment in product([True, False], repeat=len(variables)):
        env = dict(zip(variables, assignment))
        result = formula(env)
        row = " | ".join("T" if env[v] else "F" for v in variables)
        print(f"{row} | {'T' if result else 'F'}")


# Example: (p OR q) AND (NOT r)
truth_table(lambda e: (e["p"] or e["q"]) and not e["r"], ["p", "q", "r"])
