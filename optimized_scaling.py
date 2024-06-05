import math
import csv
from pathlib import Path

WORKING_DATAS_PATH = Path(__file__).parent / "data" / "working_datas.csv"
DATASET_1_PATH = Path(__file__).parent / "data" / "dataset1_Python+P7.csv"
DATASET_2_PATH = Path(__file__).parent / "data" / "dataset2_Python+P7.csv"
CLIENT_MAX_AMOUNT = 500
NAME_KEY = "name"
PRICE_KEY = "price"
PROFIT_KEY = "profit"
PROFIT_AMOUNT_KEY = "amount_profit"

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
        action[PRICE_KEY], action[PROFIT_KEY] = float(action[PRICE_KEY]), float(action[PROFIT_KEY])


def calculate_amount_profit(all_actions: list[dict]):
    """Calcule et ajoute à chacune des actions le montant de profit en euros.

    Args:
        all_actions (list[dict]): Liste des actions.
    """
    for action in all_actions:
        action[PROFIT_AMOUNT_KEY] = round(action[PRICE_KEY] * action[PROFIT_KEY] / 100, 2)


def calculate_profit_combination(combination: tuple[dict]) -> tuple[float, float]:
    """Calcule et retourne le montant total des prix et des profits d'une
    combinaison d'actions donnée.

    Args:
        combination (tuple[dict]): Liste de la combinaison d'action.

    Returns:
        tuple[float, float]: Tuple comprenant les totaux des prix et profits.
    """
    sum_price = sum(action[PRICE_KEY] for action in combination)
    sum_profits = sum(action[PROFIT_AMOUNT_KEY] for action in combination)
    
    return sum_price, sum_profits


def filter_negative_numbers(filtering_list):
    """Filtre les éléments de la liste en supprimant les éléments dont le montant du prix est négatif.

    Args:
        filtering_list (list): Liste des éléments à filtrer.

    Returns:
        list: Liste filtrée contenant uniquement les éléments dont le prix est positif.
    """
    return [element for element in filtering_list if element[PRICE_KEY] > 0]


def show_best_combination(combination_actions: list[dict]):
    """Affiche la meilleure combination d'actions entrée en paramètre.

    Args:
        combination_actions (list[dict]): Liste de la meilleure combinaison d'actions.
    """
    total_price = 0
    total_profit = 0
    border = 65 * "-"
    message = f"{border}\n| Nom\t\t| Prix (€)\t| Profit (%)\t| Profit (€)\t|\n{border}"
    for action in combination_actions:
        total_price += action[PRICE_KEY]
        total_profit += action[PROFIT_AMOUNT_KEY]
        message += f"\n| {action[NAME_KEY]}\t|\t{action[PRICE_KEY]:.2f}\t|\t{action[PROFIT_KEY]:.2f}\t|\t{action[PROFIT_AMOUNT_KEY]:.2f}\t|"
    
    message += f"\n{border}\n| TOTAL \t|\t{total_price:.2f}\t|\t\t|\t{total_profit:.2f}\t|\n{border}"
    print(message)


def scale_to_integers(number_to_factor: int | float, scale_factor=100) -> int:
    """Met à l'échelle le nombre en le multipliant par la valeur du facteur et
    retourne un nombre entier.

    Args:
        number_to_factor (int | float): Nombre à mettre à l'échelle.

    Returns:
        int: Nombre entier mit à l'échelle.
    """
    return int(number_to_factor * scale_factor)


def dynamic_algorithm(all_actions: list[dict]) -> list[dict]:
    """Récupère et retourne la meilleure combinaison possibles d'actions afin
    d'obtenir le meilleur profit dans la limite du prix indiqué dans la
    variable CLIENT_MAX_AMOUNT. (Knapsack Problem)

    Args:
        items (list[dict]): Liste de toutes les actions.

    Returns:
        list[dict]: Liste comprenant la meilleure combinaison d'actions.
    """
    max_amount = scale_to_integers(CLIENT_MAX_AMOUNT)
    actions_number = len(all_actions)
    # Création de la matrice.
    dp = [[0] * (max_amount + 1) for _ in range(actions_number + 1)]
    for i in range(1, actions_number + 1):
        price, profit = scale_to_integers(all_actions[i - 1][PRICE_KEY]), scale_to_integers(all_actions[i - 1][PROFIT_AMOUNT_KEY])
        for j in range(max_amount + 1):
            if price <= j:
                # Changement dans la matrice
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j-int(price)] + profit)
            else:
                dp[i][j] = dp[i - 1][j]

    choosed_elements = []
    # Récupération des éléments en parcourant la matrice.
    for i in range(actions_number, 0, -1):
        if dp[i][max_amount] != dp[i - 1][max_amount]:
            choosed_elements.append(all_actions[i - 1])
            price = scale_to_integers(all_actions[i - 1][PRICE_KEY])
            max_amount -= math.ceil(price)

    return choosed_elements


def run():
    datas = get_csv_datas(DATASET_1_PATH)
    convert_datas_to_integer(datas)
    calculate_amount_profit(datas)
    datas = filter_negative_numbers(datas)
    best_combination = dynamic_algorithm(datas)
    show_best_combination(best_combination)


run()
