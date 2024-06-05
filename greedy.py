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
    

def sort_by_profit_percent(all_actions):
    return sorted(all_actions, key=lambda x: x["profit"], reverse=True)

def greedy_algorithm(all_actions: list): # Naif
    combination = []
    current_amount = 0
    sorted_actions = sort_by_profit_percent(all_actions)
    for action in sorted_actions:
        if (action["price"] + current_amount) < CLIENT_MAX_AMOUNT and action["price"] > 0:
            current_amount += action["price"]
            combination.append(action)

    return combination


def run():
    datas = get_csv_datas(DATASET_2_PATH)
    convert_datas_to_integer(datas)
    calculate_amount_profit(datas)
    datas = filter_negative_numbers(datas)
    best_combination = greedy_algorithm(datas)
    show_best_combination(best_combination)
    # [print(combi[PROFIT_AMOUNT_KEY]) for combi in best_combination]
    # [print(combi[PRICE_KEY]) for combi in best_combination]


run()
