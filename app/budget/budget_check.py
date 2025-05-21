import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime


def load_budget(filepath: Path) -> dict:
    """
    Laddar budgetdata från angiven JSON-fil.

    :param filepath: Sökväg till budget.json
    :return: En dict med månadsvisa budgetar per kategori
    """
    with open(filepath, "r") as f:
        return json.load(f)


def load_transactions(filepath: Path) -> list:
    """
    Laddar transaktioner från senast importerad JSON-fil.

    :param filepath: Sökväg till transaktionsfil
    :return: En lista av transaktionsobjekt (dicts)
    """
    with open(filepath, "r") as f:
        return json.load(f)


def get_month_from_date(date_str: str) -> str:
    """
    Extraherar månad i formatet 'YYYY-MM' från ett ISO-datum.

    :param date_str: Datumsträng i ISO-format (YYYY-MM-DD)
    :return: Månadssträng 'YYYY-MM'
    """
    return datetime.fromisoformat(date_str).strftime("%Y-%m")


def summarize_transactions(transactions: list, month: str) -> dict:
    """
    Summerar transaktioner per kategori för angiven månad.
    Returnerar netto (positiva + negativa belopp).
    """
    totals = defaultdict(float)
    for tx in transactions:
        tx_month = get_month_from_date(tx["datum"])
        if tx_month == month:
            kategori = tx.get("kategori", "okänd").strip()
            totals[kategori] += tx["belopp"]
    return dict(totals)


def check_budget(budget_path: Path, transactions_path: Path):
    """
    Jämför faktisk konsumtion med budget för senaste månad.
    Kontrollera också att total budget inte överskrider inkomsten.
    """
    budget_data = load_budget(budget_path)
    transactions = load_transactions(transactions_path)

    if not transactions:
        print("⚠️ No transactions found.")
        return

    latest_month = max(get_month_from_date(tx["datum"]) for tx in transactions)
    print(f"\n🔎 Checking budget for {latest_month}...\n")

    month_data = budget_data.get(latest_month, {})
    income = month_data.get("income")
    category_budgets = month_data.get(
        "budget", month_data
    )  # fallback för platt struktur

    # Kontrollera att total budget inte överskrider inkomst
    if income is not None:
        total_budget = sum(category_budgets.values())
        if total_budget > income:
            print(
                f"❗ Total budget ({total_budget:.2f} kr) exceeds income ({income:.2f} kr)\n"
            )
        else:
            print(f"✅ Budget within income limit ({income:.2f} kr)\n")

    # Summera faktiska transaktioner
    actual = summarize_transactions(transactions, latest_month)

    # Visa alltid income först (om den finns)
    if "income" in actual:
        actual_income = actual.pop("income")
        print(
            f"income     Faktiskt: {actual_income:>8.2f} kr (registrerad inkomst i transaktioner)"
        )

    # Visa övriga kategorier i sorterad ordning (frivilligt)
    for category, actual_spent in sorted(actual.items()):
        limit = category_budgets.get(category)

        if limit is None:
            print(f"⚠️ No budget defined for category '{category}' in {latest_month}")
            continue

        balance = limit + actual_spent
        status = "✅ OK" if balance >= 0 else f"❗ OVERSPENT by {-balance:.2f} kr"

        print(
            f"{category:<10} Budget: {limit:>8.2f}  |  Actual: {actual_spent:>8.2f}  |  Balance: {balance:>8.2f}  →  {status}"
        )
