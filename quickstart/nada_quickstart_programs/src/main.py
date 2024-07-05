from nada_dsl import *

def nada_main():
    # Define the parties for the users
    user_1 = Party(name="User 1 🚉")
    user_2 = Party(name="User 2 🚉")

    # Define secret inputs for the initial seats, booking requests, and cancellation requests
    initial_seats = SecretInteger(Input(name="initial_seats", party=user_1))  # Total seats available
    book_seats_user_1 = SecretInteger(Input(name="book_seats_user_1", party=user_1))
    cancel_seats_user_1 = SecretInteger(Input(name="cancel_seats_user_1", party=user_1))
    book_seats_user_2 = SecretInteger(Input(name="book_seats_user_2", party=user_2))
    cancel_seats_user_2 = SecretInteger(Input(name="cancel_seats_user_2", party=user_2))

    # Calculate the new seat allocation after booking requests
    seats_after_booking_user_1 = (initial_seats >= book_seats_user_1).if_else(
        initial_seats - book_seats_user_1,
        initial_seats
    )
    
    seats_after_booking_user_2 = (seats_after_booking_user_1 >= book_seats_user_2).if_else(
        seats_after_booking_user_1 - book_seats_user_2,
        seats_after_booking_user_1
    )

    # Calculate the new seat allocation after cancellation requests
    seats_after_cancellation_user_1 = seats_after_booking_user_2 + cancel_seats_user_1
    seats_after_cancellation_user_2 = seats_after_cancellation_user_1 + cancel_seats_user_2

    # Output the final seat allocation
    final_seats = Output(seats_after_cancellation_user_2, "final_seats", user_1)

    # Output individual bookings and cancellations
    booked_seats_user_1 = Output(book_seats_user_1, "booked_seats_user_1", user_1)
    cancelled_seats_user_1 = Output(cancel_seats_user_1, "cancelled_seats_user_1", user_1)
    booked_seats_user_2 = Output(book_seats_user_2, "booked_seats_user_2", user_2)
    cancelled_seats_user_2 = Output(cancel_seats_user_2, "cancelled_seats_user_2", user_2)

    return [
        final_seats,
        booked_seats_user_1,
        cancelled_seats_user_1,
        booked_seats_user_2,
        cancelled_seats_user_2
    ]