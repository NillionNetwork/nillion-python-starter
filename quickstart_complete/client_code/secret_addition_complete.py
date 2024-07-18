from nada.client import Client
from nada.protocol import Protocol
from nada.protocol_parties import ProtocolParties
from nada.input import Input
from nada.output import Output

# Initialize the client
client = Client()

# Define the protocol and parties
protocol = Protocol(name="CreditCardValidation")
party1 = ProtocolParties.party("Party1")

# Define the input
cc_number = Input(name="cc_number", value="4532015112830366", party=party1)  # Example credit card number

# Define the output
is_valid_output = Output(name="is_valid_output", party=party1)

# Run the protocol
client.execute(protocol, inputs=[cc_number], outputs=[is_valid_output])

# Retrieve and print the result
result = is_valid_output.value
print(f"Credit card validity: {result}")
