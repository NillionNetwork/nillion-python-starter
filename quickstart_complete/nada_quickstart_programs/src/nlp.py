import nada_numpy as na
from my_nn import MyNN
from nada_dsl import Party

def nada_main():
    # Step 1: We use Nada NumPy wrapper to create "User" and "Provider"
    user = Party("User")
    provider = Party("Provider")

    # Step 2: Instantiate model object
    my_model = MyNN()

    # Step 3: Load model weights from Nillion network by passing model name (acts as ID)
    # In this example, the provider provides the model and the user runs inference
    my_model.load_state_from_network("my_nn", provider, na.SecretRational)

    # Step 4: Load input data to be used for inference (provided by the user)
    my_input = na.array((1, 1, 16, 16), user, "my_input", na.SecretRational)

    # Step 5: Compute inference
    # Note: completely equivalent to `my_model.forward(...)`
    result = my_model(my_input)

    # Step 6: We can use result.output() to produce the output for the user and variable name "my_output"
    return result.output(user, "my_output")
