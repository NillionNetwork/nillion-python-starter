from nada_dsl import *

def nada_main():
    # Define the parties for the voters and election officials
    voter_1 = Party(name="Voter 1 🗳️")
    voter_2 = Party(name="Voter 2 🗳️")
    election_official = Party(name="Election Official 🏛️")

    # Define secret inputs for the votes cast by each voter
    vote_voter_1 = SecretInteger(Input(name="vote_voter_1", party=voter_1))  # 1 for Candidate 1, 2 for Candidate 2
    vote_voter_2 = SecretInteger(Input(name="vote_voter_2", party=voter_2))  # 1 for Candidate 1, 2 for Candidate 2

    # Define secret inputs for the current total votes for each candidate
    total_votes_candidate_1 = SecretInteger(Input(name="total_votes_candidate_1", party=election_official))
    total_votes_candidate_2 = SecretInteger(Input(name="total_votes_candidate_2", party=election_official))

    # Calculate the new vote count for Candidate 1
    vote_count_candidate_1 = (vote_voter_1 == 1).if_else(total_votes_candidate_1 + 1, total_votes_candidate_1) + \
                             (vote_voter_2 == 1).if_else(total_votes_candidate_1 + 1, total_votes_candidate_1)

    # Calculate the new vote count for Candidate 2
    vote_count_candidate_2 = (vote_voter_1 == 2).if_else(total_votes_candidate_2 + 1, total_votes_candidate_2) + \
                             (vote_voter_2 == 2).if_else(total_votes_candidate_2 + 1, total_votes_candidate_2)

    # Output the updated vote counts for each candidate
    final_vote_count_candidate_1 = Output(vote_count_candidate_1, "final_vote_count_candidate_1", election_official)
    final_vote_count_candidate_2 = Output(vote_count_candidate_2, "final_vote_count_candidate_2", election_official)

    return [final_vote_count_candidate_1, final_vote_count_candidate_2]