from nada_dsl import *

def nada_main():
    # Define the number of voters and candidates
    num_voters = 5
    candidate_ids = [1, 2]

    # Define parties (voters)
    parties = [Party(name=f"Voter{i+1}") for i in range(num_voters)]

    # Define votes as secret integers
    votes = [SecretInteger(Input(name=f"vote{i+1}", party=parties[i])) for i in range(num_voters)]

    # Initialize secure counters for each candidate
    candidate_votes = {cid: SecretInteger(0) for cid in candidate_ids}

    # Function to validate vote
    def validate_vote(vote, candidate_ids):
        is_valid = SecretInteger(0)
        for cid in candidate_ids:
            is_valid = is_valid + vote.eq(cid)
        return is_valid.gt(0)

    # Count votes for each candidate
    for vote in votes:
        valid_vote = validate_vote(vote, candidate_ids)
        for cid in candidate_ids:
            candidate_votes[cid] = candidate_votes[cid] + vote.eq(cid) * valid_vote

    # Output the total votes for each candidate
    outputs = [Output(candidate_votes[cid], f"candidate{cid}_votes") for cid in candidate_ids]
    return outputs
