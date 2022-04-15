def specify_compartments(exposed, vaccinated, maternal, warning, compromised):
    all_compartments = []
    all_compartments.append("susceptible", "infected", "recovered")

    if exposed == True:
        all_compartments.append("exposed")
    if vaccinated == True: 
        all_compartments.append("vaccinated")
    if maternal == True:
        all_compartments.append("maternal")
    if warning == True:
        all_compartments.append("warning")
    if compromised == True:
        all_compartments.append("compromised")
    
    return all_compartments


def specify_disease_characteristics(mu, alpha, d):
    disease_characteristics = []
    disease_characteristics.append("beta", "gamma")

    if mu == True:
        disease_characteristics.append("mu")
    if alpha == True:
        disease_characteristics.append("alpha")
    if d == True:
        disease_characteristics.append("d")
    
    return disease_characteristics


def determine_base_equations(all_compartments):
    

