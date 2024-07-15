from nada_dsl import *

def create_parties(num_managers):
    parties = []
    for i in range(num_managers):
        parties.append(Party(name="Manager" + str(i)))
    return parties

def initialize_inputs(num_managers, num_employees, parties):
    employee_scores = []
    for e in range(num_employees):
        employee_scores.append([])
        for m in range(num_managers):
            employee_scores[e].append(
                SecretUnsignedInteger(
                    Input(name="m" + str(m) + "_e" + str(e), party=parties[m])
                )
            )
    return employee_scores

def calculate_average_scores(num_managers, num_employees, employee_scores, output_party):
    avg_scores = []
    for e in range(num_employees):
        total_score = employee_scores[e][0]
        for m in range(1, num_managers):
            total_score += employee_scores[e][m]
        average_score = total_score / UnsignedInteger(num_managers)
        avg_scores.append(Output(average_score, "avg_score_e" + str(e), output_party))
    return avg_scores

def validate_scores(num_managers, num_employees, employee_scores, max_score, output_party):
    score_validations = []
    reveal_cheating = []
    for e in range(num_employees):
        for m in range(num_managers):
            score = employee_scores[e][m]
            is_valid = score <= UnsignedInteger(max_score)
            score_validations.append(Output(is_valid, "check_score_m" + str(m) + "_e" + str(e), output_party))
            reveal_cheat = is_valid.if_else(UnsignedInteger(0), score)
            reveal_cheating.append(Output(reveal_cheat, "if_cheat_open_m" + str(m) + "_e" + str(e), output_party))
    return score_validations, reveal_cheating

def nada_main():
    num_managers = 3
    num_employees = 2
    max_allowed_score = 10

    parties = create_parties(num_managers)
    output_party = Party(name="OutputParty")

    employee_scores = initialize_inputs(num_managers, num_employees, parties)

    avg_scores = calculate_average_scores(num_managers, num_employees, employee_scores, output_party)
    score_validations, reveal_cheating = validate_scores(num_managers, num_employees, employee_scores, max_allowed_score, output_party)

    results = avg_scores + score_validations + reveal_cheating
    return results

nada_main()