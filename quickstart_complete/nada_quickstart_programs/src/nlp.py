import nada_numpy as na
from my_nn import MyNN
from nada_dsl import Party

def nada_main():
    user = Party("User")
    provider = Party("Provider")

    my_model = MyNN()

    # Model weights are loaded
    my_model.load_state_from_network("my_nn", provider, na.SecretRational)

    # Input data is loaded
    my_input = na.array((1, 1, 16, 16), user, "my_input", na.SecretRational)

    result = my_model(my_input)

    return result.output(user, "my_output")
