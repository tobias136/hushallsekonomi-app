import json
from pathlib import Path
from datetime import datetime


def extract_income(transactions: list) -> float:
    """
    Summerar alla transaktioner där kategorin är 'income' eller transaktionstyp är 'Lön'.
    """
    return sum(
        tx["belopp"]
        for tx in transactions
        if tx.get("kategori") == "income" or tx.get("transaktionstyp") == "Lön"
    )


def get_month_from_transaction_file(filepath: Path) -> tuple[str, list]:
    """
    Returnerar första transaktionens månad i format 'YYYY-MM' och hela transaktionslistan.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        transactions = json.load(f)
    if not transactions:
        raise ValueError("Transaktionsfilen är tom.")
    return (
        datetime.fromisoformat(transactions[0]["datum"]).strftime("%Y-%m"),
        transactions,
    )


def create_monthly_budget(
    transactions_path: Path, budget_path: Path = Path("data/budget.json")
):
    month, transactions = get_month_from_transaction_file(transactions_path)
    income = extract_income(transactions)

    print(f"📆 Månad: {month}")

    if income == 0.0:
        while True:
            try:
                income = float(
                    input(
                        "⚠️ Ingen lön hittades i transaktionerna. Ange förväntad inkomst manuellt: "
                    )
                )
                break
            except ValueError:
                print("❌ Ange ett giltigt nummer.")
    else:
        print(f"💰 Upptäckt inkomst: {income:.2f} kr")

    categories = ["needs", "wants", "culture", "savings"]
    budget_data = {}

    for cat in categories:
        while True:
            try:
                val = float(input(f"Ange budget för '{cat}': "))
                budget_data[cat] = val
                break
            except ValueError:
                print("❌ Ange ett giltigt nummer.")

    # Ladda befintlig budget
    if budget_path.exists():
        with open(budget_path, "r", encoding="utf-8") as f:
            all_budgets = json.load(f)
    else:
        all_budgets = {}

    all_budgets[month] = {"income": income, "budget": budget_data}

    budget_path.parent.mkdir(parents=True, exist_ok=True)
    with open(budget_path, "w", encoding="utf-8") as f:
        json.dump(all_budgets, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Budget för {month} sparad i {budget_path}")
