import nada_numpy as na
from nada_ai.linear_model import LogisticRegression

def nada_main():
    # Set precision
    na.set_log_scale(32)
    
    # Create "Party0" and "Party1"
    parties = na.parties(2)
    
    # Instantiate logistic regression object
    # Using a dataset with 12 features and 1 output feature for binary classification
    feature_count = 12
    output_count = 1
    my_model = LogisticRegression(in_features=feature_count, out_features=output_count)
    
    # Load model weights from Nillion network by passing model name
    my_model.load_state_from_network("my_logistic_model", parties[0], na.SecretRational)
    
    # Load input data to be used for inference
    my_input = na.array((feature_count,), parties[1], "my_input", na.SecretRational)
    
    result = my_model.forward(my_input)
    
    return na.output(result, parties[1], "my_output")

