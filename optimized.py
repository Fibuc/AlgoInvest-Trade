import math

import utils, constants

def sort_by_profit_percent(all_actions):
    return sorted(all_actions, key=lambda x: x["profit"], reverse=True)

def greedy_algorithm(all_actions: list): # Naif
    combination = []
    current_amount = 0
    sorted_actions = sort_by_profit_percent(all_actions)
    for action in sorted_actions:
        if (action["price"] + current_amount) < constants.CLIENT_MAX_AMOUNT and action["price"] > 0:
            current_amount += action["price"]
            combination.append(action)

    return combination

def dynamic_algorithm(items: list[tuple[str, float, float]]) -> list:
    n = len(items)
    max_weight = constants.CLIENT_MAX_AMOUNT
    # Création de la matrice. (x: montant, y: élément)
    dp = [[0] * (max_weight + 1) for _ in range(n + 1)]

    # Pour chaque élément dans la liste.
    for i in range(1, n + 1): # Démarre à l'indice 1 car 1ère ligne est n[0] +1 pour arriver 21 et non 20.

        # Attribution des valeurs de l'élément en cours.
        name, weight, value = items[i - 1]["name"], items[i - 1]["price"], items[i - 1]["amount_profit"]

        # Pour chaque entier du montant max (O à 500).
        for w in range(max_weight + 1): # +1 pour arriver à 500 et non 499.

            # Si montant élément inférieur à entier du montant en cours.
            if weight <= w:
            # Changement dans la matrice
                # Evaluer max entre valeur dans la ligne précédente et
                # la valeur max de la ligne précédente de la colonne sans poids objet + le poids de l'objet
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w-math.ceil(weight)] + value)
            
            # Sinon est égal à la ligne précédente.
            else:
                dp[i][w] = dp[i - 1][w]

    # Récupérer les éléments choisis dans une liste
    w = max_weight
    choosed_elements = []

    # Parcours de la liste inversée.
    for i in range(n, 0, -1):
        # Si élément choisis pour le poid est différent de celui de la ligne précédente = Utilisation élément.
        if dp[i][w] != dp[i - 1][w]:
            choosed_elements.append(items[i - 1]) # Ajout de l'élément à la liste
            weight = items[i - 1]["price"]
            w -= math.ceil(weight) # Déduction de la valeur maximale, le montant de l'élément. 

    return choosed_elements
                


if __name__ == '__main__':
    datas = utils.get_csv_datas(constants.WORKING_DATAS_PATH)
    utils.convert_datas_to_integer(datas)
    utils.calculate_amount_profit(datas)
    best_combination = dynamic_algorithm(datas)
    # best_combination = greedy_algorithm(datas)
    utils.show_best_combination(best_combination)
    # utils.show_best_actions(best_combination)



