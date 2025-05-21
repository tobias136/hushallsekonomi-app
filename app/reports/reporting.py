import json
import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path


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


def save_report_to_csv(summary, out_dir="reports"):
    """Save the report as separate CSV files per month."""
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    for month in summary:
        filename = Path(out_dir) / f"rapport_{month}.csv"
        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Kategori", "Summa (SEK)"])
            for category, total in sorted(summary[month].items()):
                writer.writerow([category, f"{total:.2f}"])
        print(f"💾 Sparad: {filename}")


def save_report_to_markdown(summary, out_dir="reports"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    for month in summary:
        filename = Path(out_dir) / f"report_{month}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Monthly Report – {month}\n\n")
            f.write("| Category       | Amount (SEK) |\n")
            f.write("|----------------|--------------|\n")
            for category, total in sorted(summary[month].items()):
                f.write(f"| {category:<14} | {total:>12.2f} |\n")
        print(f"💾 Saved: {filename}")


def save_report_to_json(summary, out_dir="reports"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    for month in summary:
        filename = Path(out_dir) / f"report_{month}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(summary[month], f, indent=2, ensure_ascii=False)
        print(f"💾 Saved: {filename}")


def generate_latest_report(data_dir="data", export_format=None):
    """
    Find the latest imported JSON file and generate a report from it.
    Optionally save the report to file.

    Args:
        data_dir (str): Folder with import_*.json files.
        export_format (str|None): 'csv' to save, otherwise only print.
    """
    files = sorted(Path(data_dir).glob("import_*.json"), reverse=True)
    if not files:
        print("❌ Ingen importfil hittad i mappen 'data/'.")
        return

    latest_file = files[0]
    print(f"📂 Läser fil: {latest_file.name}")
    transactions = load_transactions(latest_file)
    summary = group_by_month_and_category(transactions)
    print_report(summary)

    if export_format == "csv":
        save_report_to_csv(summary)
    elif export_format == "markdown":
        save_report_to_markdown(summary)
    elif export_format == "json":
        save_report_to_json(summary)
