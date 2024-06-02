import csv
from pathlib import Path

from prettytable import PrettyTable

import constants


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

def calculate_amount_profit(all_actions: list[dict]):
    for action in all_actions:
        action["amount_profit"] = round(action["price"] * action["profit"] / 100, 2)


def calculate_profit_combination(combination: tuple[dict]) -> tuple[float, float]:
    """Calcule et retourne le montant total des prix et des profits d'une
    combinaison d'actions donnée.

    Args:
        combination (tuple[dict]): Liste de la combinaison d'action.

    Returns:
        tuple[float, float]: Tuple comprenant les totaux des prix et profits.
    """
    sum_price = sum(action["price"] for action in combination)
    sum_profits = sum(action["amount_profit"] for action in combination)
    
    return sum_price, sum_profits


def show_best_combination(combination_actions: list[dict[str, str | float]]):
    """Affiches les actions présente dans la combinaison ainsi que le prix total
    et le profit maximum de celle-ci.

    Args:
        combination_actions (list[dict]): Liste des actions de la combinaison.
        total_price (float): Prix total de la combinaison.
        total_profit (float): Profit total de la combinaison.
    """
    table = PrettyTable()
    table.title = f"Meilleures actions de: {constants.WORKING_DATAS_PATH.name}"
    table.field_names = ["Nom", "Prix (€)", "Profit (%)", "Profit (€)"]
    for name in table.field_names:
        if name == "Nom":
            table.align[name] = "l"
            continue
        table.align[name] = "r"

    total_price = 0
    total_profit = 0
    for action in combination_actions[::-1]:
        total_next = False
        if action == combination_actions[0]:
            total_next = True

        table.add_row([action['name'], f"{action['price']:.2f}", f"{action['profit']:.2f}", f"{action['amount_profit']:.2f}"], divider=total_next)
        total_price += action['price']
        total_profit += action['amount_profit']

    table.add_row(["TOTAL", f"{total_price:.2f}", "", f"{total_profit:.2f}"])
    print()
    print(table)