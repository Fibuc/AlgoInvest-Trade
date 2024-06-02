from itertools import combinations

import utils, constants

def sort_by_price(all_actions):
    return sorted(all_actions, key=lambda x: x["price"], reverse=True)

def get_best_combination(all_actions: list[dict[str, str | float]]) -> tuple[tuple, float, float]:
    """Récupère et retourne la meilleure combinaison possibles d'actions afin
    d'obtenir le meilleur profit dans la limite du prix indiqué dans la
    variable CLIENT_MAX_AMOUNT. (Knapsack Problem)

    Args:
        all_actions (list[dict]): Liste de toutes les actions.

    Returns:
        tuple[tuple, float, float]: Tuple comprenant les actions, le prix total
        et le profit total de la meilleur combinaison.
    """
    nb_combination = 0
    max_profits = 0
    best_combination = None
    for r in range(1, len(all_actions) + 1):
        for combination in combinations(all_actions, r):
            total_price, total_profit = utils.calculate_profit_combination(combination)
            nb_combination += 1
            if total_price <= constants.CLIENT_MAX_AMOUNT and total_profit > max_profits:
                max_profits = total_profit
                best_combination = combination
    
    return best_combination


if __name__ == '__main__':
    datas = utils.get_csv_datas(constants.WORKING_DATAS_PATH)
    utils.convert_datas_to_integer(datas)
    utils.calculate_amount_profit(datas)
    best_combination = get_best_combination(datas)
    # # utils.show_best_actions(best_combination)
    utils.show_best_combination(best_combination)
    # print(sort_by_price(datas))


