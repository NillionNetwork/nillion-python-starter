def digest_plurality_vote_honest_result(dict_result, nr_candidates, nr_voters):

    # TODO: complete there the code to digest the output of the honest version

    print("Update 'digest_plurality_vote_honest_result()' functions to digest the result.")

    return None


def digest_plurality_vote_dishonest_with_abort_result(dict_result, nr_candidates, nr_voters):

    # TODO: complete there the code to digest the output of the dishonest with abort version

    print("Update 'digest_plurality_vote_dishonest_with_abort_result()' functions to digest the result.")

    return None


def digest_plurality_vote_robust_result(dict_result, nr_candidates, nr_voters):
    """
    Digests the robust result of a plurality voting process, identifying the winner,
    the votes per candidate, and any potential cheaters.

    Parameters:
    - dict_result (dict): A dictionary containing the robust result of the plurality
                          voting process. It should contain keys for final vote counts
                          for each candidate, checks for sum and product rules per voter,
                          and actions if cheating is detected.
    - nr_candidates (int): The total number of candidates in the voting process.
    - nr_voters (int): The total number of voters in the voting process.

    Returns:
    - winner (int): The index of the winning candidate.
    - votes_per_candidate (list): A list containing the number of votes received by
                                   each candidate.
    - cheaters (list): A list containing the IDs of any potential cheaters.
    """

    # check cheaters
    set_of_cheaters = set()
    for v in range(nr_voters):
        if dict_result["check_sum_v"+str(v)] != nr_candidates + 1:
            # add the voter id to set_of_cheaters
            set_of_cheaters.add(v)
        for c in range(nr_candidates):
            if dict_result["check_prod_v"+str(v)+"_c"+str(c)] != 0:
                # add the voter id to set_of_cheaters
                set_of_cheaters.add(v)

    # collect final votes
    votes_per_candidate = []
    for c in range(nr_candidates):
        # read nr of votes for candidate 'c'
        votes_per_candidate.append(dict_result["final_vote_count_c"+str(c)])
    # revert action of cheaters for all candidates
    for cheater in set_of_cheaters:
        # if sum rule was broken
        if dict_result["check_sum_v"+str(cheater)] != nr_candidates + 1:
            for c in range(nr_candidates):
                votes_per_candidate[c] -= dict_result["if_sum_cheat_open_v"+str(cheater)+"_c"+str(c)]
        # if product rule was broken
        else:
            for c in range(nr_candidates):
                votes_per_candidate[c] -= dict_result["if_prod_cheat_open_v"+str(cheater)+"_c"+str(c)]
        
    # define winner
    winner = max(range(len(votes_per_candidate)), key=lambda i: votes_per_candidate[i])
    
    return winner, votes_per_candidate, list(set_of_cheaters)

