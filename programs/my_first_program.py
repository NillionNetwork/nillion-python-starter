from nada_dsl import *

def nada_main():
    num_voters = 5
    candidate_ids = [1, 2]

    parties = [Party(name=f"Voter{i+1}") for i in range(num_voters)]
    votes = [SecretInteger(Input(name=f"vote{i+1}", party=parties[i])) for i in range(num_voters)]
    candidate_votes = {cid: SecretInteger(0) for cid in candidate_ids}

    def validate_vote(vote, candidate_ids):
        is_valid = SecretInteger(0)
        for cid in candidate_ids:
            is_valid = is_valid + vote.eq(cid)
        return is_valid.gt(0)

    for vote in votes:
        valid_vote = validate_vote(vote, candidate_ids)
        for cid in candidate_ids:
            candidate_votes[cid] = candidate_votes[cid] + vote.eq(cid) * valid_vote

    outputs = [Output(candidate_votes[cid], f"candidate{cid}_votes") for cid in candidate_ids]
    return outputs
