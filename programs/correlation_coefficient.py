from nada_dsl import *

def nada_main():
    """
    This program computes the correlation coefficient between two vectors. 
    
    In this example we assume there are two parties P0 and P1. 
    P0 provides 10 points (x_i, y_i) and P1 provides 10 pointss (x_j, y_j).
    """

    nr_parties = 2
    p0_points = 10
    p1_points = 10
    precision = 5
    total_points = p0_points + p1_points

    # Create parties
    parties = []
    for i in range(nr_parties):
        parties.append(Party(name="Party" + str(i)))
    outparty = Party(name="OutParty")


    # Build x and y vector
    xi_vector = []
    yi_vector = []
    # Party 0 input
    for i in range(p0_points):
        xi_vector.append(SecretInteger(Input(name="x" + str(i), party=parties[0])))
        yi_vector.append(SecretInteger(Input(name="y" + str(i), party=parties[0])))
    # Party 1 input
    for i in range(p1_points):
        xi_vector.append(SecretInteger(Input(name="x" + str(i + p0_points), party=parties[1])))
        yi_vector.append(SecretInteger(Input(name="y" + str(i + p0_points), party=parties[1])))

    # Compute the following values:
    #   sum_x = Σ x_i
    #   sum_y = Σ y_i
    #   sum_xy = Σ x_i.y_i
    #   sum_xx = Σ x_i.x_i
    #   sum_yy = Σ y_i.y_i
    sum_x = xi_vector[0]
    sum_y = yi_vector[0]
    sum_xy = xi_vector[0] * yi_vector[0]
    sum_xx = xi_vector[0] * xi_vector[0]
    sum_yy = yi_vector[0] * yi_vector[0]
    for i in range(1, total_points):
        sum_x += xi_vector[i]
        sum_y += yi_vector[i]
        sum_xy += xi_vector[i] * yi_vector[i]
        sum_xx += xi_vector[i] * xi_vector[i]
        sum_yy += yi_vector[i] * yi_vector[i]

    # Build the formula:
    #                               (n * sum_xy - sum_x * sum_y)
    #   (r_xy)^2 = -------------------------------------------------------------
    #               (n * sum_xx - sum_x * sum_x) * (n * sum_yy - sum_y * sum_y)
    n = Integer(total_points)
    n_times_sum_xy = n * sum_xy
    sum_x_times_sum_y = sum_x * sum_y
    ld = n * sum_xx - sum_x * sum_x
    rd = n * sum_yy - sum_y * sum_y

    numerator = n_times_sum_xy - sum_x_times_sum_y
    denominator = ld * rd
    sq_numerator = numerator * numerator * Integer(10**precision)
    r2 = sq_numerator / denominator

    # If sign == true, sign is positive
    #            else, sign is negative
    sign = n_times_sum_xy > sum_x_times_sum_y

    return [(Output(r2, "correlation_coefficient_squared", outparty)), (Output(sign, "sign", outparty))] 