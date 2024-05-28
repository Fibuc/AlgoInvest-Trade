import csv
from pathlib import Path
from itertools import combinations


CLIENT_MAX_AMOUNT = 500
WORKING_DATAS_PATH = Path(__file__).parent / "data" / "working_datas.csv"


def get_csv_datas(file_path: Path | str) -> list[dict]:
    """Récupère et retourne les données présentes dans le fichier CSV
    indiqué en argument.

    Args:
        file_path (Path | str): Chemin d'accès au fichier CSV.

    Returns:
        list[dict]: Liste de dictionnaire comprenant toutes les lignes du fichier CSV.
    """
    all_actions = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            all_actions.append(row)
    
    return all_actions


def convert_datas_to_integer(all_actions: list[dict]):
    """Convertie les données des prix et profits des actions en nombre décimaux.

    Args:
        all_actions (list[dict]): Liste des actions.
    """
    for action in all_actions:
        action["price"], action["profit"] = float(action["price"]), float(action["profit"])


def calculate_profit(combination: tuple[dict]) -> tuple[float, float]:
    """Calcule et retourne le montant total des prix et des profits d'une
    combinaison d'actions donnée.

    Args:
        combination (tuple[dict]): Liste de la combinaison d'action.

    Returns:
        tuple[float, float]: Tuple comprenant les totaux des prix et profits.
    """
    sum_price = sum(action["price"] for action in combination)
    sum_profits = sum(
        action["price"] * action["profit"] / 100
        for action in combination
        )
    
    return sum_price, sum_profits


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
    max_profits = 0
    max_prices = 0
    best_combination = None
    for r in range(1, len(all_actions) + 1):
        for combination in combinations(all_actions, r):
            total_price, total_profit = calculate_profit(combination)
            if total_price <= CLIENT_MAX_AMOUNT and total_profit > max_profits:
                max_profits = total_profit
                max_prices = total_price
                best_combination = combination
    
    return best_combination, max_prices, max_profits


def show_best_combination(
        combination_actions: list[dict[str, str | float]], total_price: float,
        total_profit: float):
    """Affiches les actions présente dans la combinaison ainsi que le prix total
    et le profit maximum de celle-ci.

    Args:
        combination_actions (list[dict]): Liste des actions de la combinaison.
        total_price (float): Prix total de la combinaison.
        total_profit (float): Profit total de la combinaison.
    """
    for i, action in enumerate(combination_actions, start=1):
        print(f"Choix {i}: \nNom: {action["name"]}\nPrix: {action["price"]}€\nProfit: {action["profit"]}%\n")

    print(f"Coût total: {total_price}€\nProfit total: {total_profit}€")

if __name__ == '__main__':
    datas = get_csv_datas(WORKING_DATAS_PATH)
    convert_datas_to_integer(datas)
    best_combination, total_price, total_profit = get_best_combination(datas)
    show_best_combination(best_combination, total_price, total_profit)


