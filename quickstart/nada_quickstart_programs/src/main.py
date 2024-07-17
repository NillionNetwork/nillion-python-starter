from nada_dsl import *


def initialize_participants(nr_participants):
    """
    Initialize participants with unique identifiers.

    Parameters:
    - nr_participants (int): Number of participants.

    Returns:
    - participants (list): List of Party objects representing participants.
    """
    participants = []
    for i in range(nr_participants):
        participants.append(Party(name="Participant" + str(i)))
    return participants


def inputs_initialization(nr_participants, participants):
    """
    Initialize inputs for each participant's chosen number.

    Parameters:
    - nr_participants (int): Number of participants.

    Returns:
    - chosen_numbers (list): List representing chosen numbers for each participant.
    """
    chosen_numbers = []
    for p in range(nr_participants):
        chosen_numbers.append(
            SecretUnsignedInteger(Input(name="chosen_number_p" + str(p), party=participants[p]))
        )
    return chosen_numbers


def determine_winner(nr_participants, chosen_numbers, winning_number, outparty):
    """
    Determine the winner based on the closest match to the winning number.

    Parameters:
    - nr_participants (int): Number of participants.
    - chosen_numbers (list): List representing chosen numbers for each participant.
    - winning_number (UnsignedInteger): The predetermined winning number.

    Returns:
    - winner_output (Output): Output object representing the winner's identifier.
    """
    closest_diff = UnsignedInteger(2**32 - 1)  # Initialize with a large number
    winner_id = UnsignedInteger(0)

    for p in range(nr_participants):
        diff = (chosen_numbers[p] - winning_number).abs()
        is_closer = diff < closest_diff
        closest_diff = is_closer.if_else(diff, closest_diff)
        winner_id = is_closer.if_else(UnsignedInteger(p), winner_id)

    winner_output = Output(winner_id, "winner_id", outparty)
    return winner_output


def nada_main():
    # Number of participants
    nr_participants = 3

    # Predetermined winning number
    winning_number = UnsignedInteger(50)  # You can set this to any number

    # Parties initialization
    participants = initialize_participants(nr_participants)
    outparty = Party(name="OutParty")

    # Inputs initialization
    chosen_numbers = inputs_initialization(nr_participants, participants)

    # Determine the winner
    winner_output = determine_winner(nr_participants, chosen_numbers, winning_number, outparty)

    # Output the result
    return [winner_output]
