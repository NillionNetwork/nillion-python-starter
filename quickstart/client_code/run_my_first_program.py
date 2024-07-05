from nada_dsl import *

def initialize_managers(nr_managers):
    """
    Initialize managers with unique identifiers.

    Parameters:
    - nr_managers (int): Number of managers.

    Returns:
    - managers (list): List of Party objects representing managers.
    """
    managers = []
    for i in range(nr_managers):
        managers.append(Party(name="Manager" + str(i)))

    return managers

def inputs_initialization(nr_managers, nr_employees, managers):
    """
    Initialize inputs for performance scores per employee.

    Parameters:
    - nr_managers (int): Number of managers.
    - nr_employees (int): Number of employees.

    Returns:
    - scores_per_employee (list): List of lists representing scores per employee.
    """
    scores_per_employee = []
    for e in range(nr_employees):
        scores_per_employee.append([])
        for m in range(nr_managers):
            scores_per_employee[e].append(
                SecretUnsignedInteger(
                    Input(name="m" + str(m) + "_e" + str(e), party=managers[m])
                )
            )

    return scores_per_employee

def compute_average_scores(nr_managers, nr_employees, scores_per_employee, outparty):
    """
    Compute the average scores for each employee.

    Parameters:
    - nr_managers (int): Number of managers.
    - nr_employees (int): Number of employees.
    - scores_per_employee (list): List of lists representing scores per employee.

    Returns:
    - avg_scores (list): List of Output objects representing average scores for each employee.
    """
    avg_scores = []
    for e in range(nr_employees):
        total_score = scores_per_employee[e][0]
        for m in range(1, nr_managers):
            total_score += scores_per_employee[e][m]
        average_score = total_score / UnsignedInteger(nr_managers)
        avg_scores.append(Output(average_score, "avg_score_e" + str(e), outparty))

    return avg_scores

def verify_scores(nr_managers, nr_employees, scores_per_employee, max_score, outparty):
    """
    Check if any score exceeds the allowed maximum score.

    Parameters:
    - nr_managers (int): Number of managers.
    - nr_employees (int): Number of employees.
    - scores_per_employee (list): List of lists representing scores per employee.

    Returns:
    - score_checks (list): List of Output objects representing score checks for each employee.
    - if_cheat_open (list): List of Output objects representing revealed scores of cheating managers.
    """
    score_checks = []
    if_cheat_open = []
    for e in range(nr_employees):
        for m in range(nr_managers):
            score = scores_per_employee[e][m]
            check = score <= UnsignedInteger(max_score)
            score_checks.append(Output(check, "check_score_m" + str(m) + "_e" + str(e), outparty))
            reveal_cheat = check.if_else(UnsignedInteger(0), score)
            if_cheat_open.append(Output(reveal_cheat, "if_cheat_open_m" + str(m) + "_e" + str(e), outparty))

    return score_checks, if_cheat_open

def nada_main():
    # Compiled-time constants
    nr_managers = 3
    nr_employees = 2
    max_score = 10  # Example maximum score allowed

    # Parties initialization
    managers = initialize_managers(nr_managers)
    outparty = Party(name="OutParty")

    # Inputs initialization
    scores_per_employee = inputs_initialization(nr_managers, nr_employees, managers)

    # Computation
    # Compute average scores
    avg_scores = compute_average_scores(nr_managers, nr_employees, scores_per_employee, outparty)
    # Check score validity
    score_checks, if_cheat_open = verify_scores(nr_managers, nr_employees, scores_per_employee, max_score, outparty)

    # Output
    results = avg_scores + score_checks + if_cheat_open
    return results

# Run the main function
nada_main()
