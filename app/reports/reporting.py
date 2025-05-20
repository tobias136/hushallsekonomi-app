import json
from collections import defaultdict
from datetime import datetime


def load_transactions(filepath):
    """
    Load transactions from a JSON file.

    Args:
        filepath (str): Path to the JSON file containing transaction data.

    Returns:
        list[dict]: List of transactions with fields such as 'date', 'amount', and 'category'.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def group_by_month_and_category(transactions):
    """
    Group transactions by month and category, summing the amounts.

    Args:
        transactions (list[dict]): List of transaction records.

    Returns:
        dict: Nested dictionary of the form {month: {category: total_amount}}.
    """
    summary = defaultdict(lambda: defaultdict(float))
    for tx in transactions:
        date = datetime.fromisoformat(tx["datum"])
        month = date.strftime("%Y-%m")
        category = tx.get("kategori", "uncategorized")
        amount = float(tx["belopp"])
        summary[month][category] += amount
    return summary


def print_report(summary):
    """
    Print a formatted summary report to the terminal.

    Args:
        summary (dict): Nested dictionary {month: {category: total_amount}} to be printed.
    """
    for month in sorted(summary):
        print(f"\n=== {month} ===")
        for category, total in summary[month].items():
            print(f"{category:15}: {total:.2f} SEK")


def generate_report(filepath):
    """
    Full reporting pipeline: load data, process it, and print the result.

    Args:
        filepath (str): Path to the input transaction JSON file.
    """
    transactions = load_transactions(filepath)
    summary = group_by_month_and_category(transactions)
    print_report(summary)
