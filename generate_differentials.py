"""A program to create differential equations based on compartments for modeling."""


from math import gamma
from pyexpat import model
from collections import defaultdict
import re
from unittest.loader import VALID_MODULE_NAME

from regex import E


def basic_equations(S, I, R, alpha, mu, beta, gamma):
    """Define the equations for an SIR model."""
    dS = alpha - (mu * S) - (beta * I * S)
    dI = (beta * I * S) - ((gamma - mu) * I)
    dR = (gamma * I) - (mu * R)

    return dS, dI, dR


def model_relationships():
    relationship_dict = defaultdict(dict)

    relationship_dict["S"]["I"] = False, True, "beta"
    relationship_dict["S"]["R"] = False, False, "n/a"
    relationship_dict["S"]["E"] = False, True, "beta"
    relationship_dict["S"]["V"] = False, True, "vaccination"
    relationship_dict["S"]["D"] = False, False, "n/a"

    relationship_dict["I"]["S"] = True, False, "beta"
    relationship_dict["I"]["R"] = False, True, "gamma"
    relationship_dict["I"]["E"] = True, False, "beta"
    relationship_dict["I"]["V"] = False, False, "n/a"
    relationship_dict["I"]["D"] = False, True, "mu"

    relationship_dict["R"]["S"] = False, False, "n/a"
    relationship_dict["R"]["I"] = True, False, "gamma"
    relationship_dict["R"]["E"] = False, False, "n/a"
    relationship_dict["R"]["V"] = False, False, "n/a"
    relationship_dict["R"]["D"] = False, False, "n/a"

    relationship_dict["E"]["S"] = True, False, "beta"
    relationship_dict["E"]["I"] = False, True, "beta"
    relationship_dict["E"]["R"] = False, True, "gamma"
    relationship_dict["E"]["V"] = False, False, "n/a"
    relationship_dict["E"]["D"] = False, True, "mu"

    relationship_dict["V"]["S"] = True, False, "vaccination"
    relationship_dict["V"]["I"] = False, False, "n/a"
    relationship_dict["V"]["R"] = False, False, "n/a"
    relationship_dict["V"]["E"] = True, False, "vaccination"
    relationship_dict["V"]["D"] = False, False, "n/a"

    relationship_dict["D"]["S"] = True, False, "mu"
    relationship_dict["D"]["I"] = True, False, "mu"
    relationship_dict["D"]["R"] = False, False, "n/a"
    relationship_dict["D"]["E"] = False, False, "n/a"
    relationship_dict["D"]["V"] = False, False, "n/a"

    return relationship_dict


def determine_compartments(S, I, R, E, V, D):
    specified_compartments = []
    if S == True:
        specified_compartments.append("S")
    if I == True:
        specified_compartments.append("I")
    if R == True:
        specified_compartments.append("R")
    if E == True:
        specified_compartments.append("E")
    if V == True:
        specified_compartments.append("V")
    if D == True:
        specified_compartments.append("D")

    return specified_compartments


def find_correct_variable(
    input_string, S, I, R, E, V, D, beta_value, gamma_value, vacc_value, mu_value
):
    if input_string == "S":
        return S
    if input_string == "I":
        return I
    if input_string == "R":
        return R
    if input_string == "E":
        return E
    if input_string == "V":
        return V
    if input_string == "D":
        return D
    if input_string == "beta":
        return beta_value
    if input_string == "gamma":
        return gamma_value
    if input_string == "mu":
        return mu_value
    if input_string == "vaccination":
        return vacc_value


def create_differentials(
    specified_compartments,
    relationship_dict,
    S,
    I,
    R,
    E,
    V,
    D,
    beta_value,
    gamma_value,
    vacc_value,
    mu_value,
):
    # Iterate through list of specified compartments
    equation_list = []
    final_equation = 0
    for compartment in specified_compartments:
        # Iterate through relationship_dict, looking for the matching compartment
        for key, value in relationship_dict.items():
            key_for_equation = find_correct_variable(
                key, S, I, R, E, V, D, beta_value, gamma_value, vacc_value, mu_value
            )
            for new_key, new_value in value.items():
                print(new_key)
                if new_key == compartment:
                    new_key_equation = find_correct_variable(
                        new_key,
                        S,
                        I,
                        R,
                        E,
                        V,
                        D,
                        beta_value,
                        gamma_value,
                        vacc_value,
                        mu_value,
                    )
                    first_part_equation = 0
                    take_away = new_value[0]
                    add_to = new_value[1]
                    rate = new_value[2]
                    rate_equation = find_correct_variable(
                        rate,
                        S,
                        I,
                        R,
                        E,
                        V,
                        D,
                        beta_value,
                        gamma_value,
                        vacc_value,
                        mu_value,
                    )
                    if take_away == True:
                        first_part_equation = (
                            -new_key_equation * key_for_equation * rate_equation
                        )
                        equation_list.append(first_part_equation)
                    if add_to == True:
                        second_part_equation = (
                            new_key_equation * key_for_equation * rate_equation
                        )
                        equation_list.append(second_part_equation)

                    for equation in equation_list:
                        final_equation = final_equation + equation
                    print(final_equation)


if __name__ == "__main__":
    relationship_dict = model_relationships()
    specified_compartments = determine_compartments(
        True, True, True, False, False, False
    )

    create_differentials(
        specified_compartments,
        relationship_dict,
        1000,
        1,
        0,
        0,
        0,
        0,
        0.1,
        0.3,
        0.2,
        0.2,
    )
