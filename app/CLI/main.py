import sys
import os
import click
import json
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from scripts.import_transactions import import_csv, save_to_json
from app.categorizer.kategorisering import (
    ladda_kategorier,
    spara_kategorier,
    kategorisera_transaktion,
)
from app.reports.reporting import generate_report, generate_latest_report
from app.budget.budget_check import check_budget

# === Globala konstanter ===
BUDGET_PATH = Path("data/budget.json")
DATA_DIR = Path("data/")


@click.group()
def cli():
    """Hushållsekonomi CLI-verktyg."""
    pass


@cli.command()
@click.option(
    "--file", required=True, type=click.Path(exists=True), help="Path to CSV file"
)
def importera(file):
    """Importera transaktioner från en CSV-fil och kategorisera dem."""
    click.echo(f"Importerar från {file}...")

    # Importera transaktioner
    transactions = import_csv(file)
    click.echo(f"{len(transactions)} transaktioner importerade.")

    if transactions:
        # Ladda befintliga kategorier
        kategorier = ladda_kategorier()

        # Kategorisera varje transaktion
        for transaction in transactions:
            # Säkerställ att nödvändiga fält finns
            if "transaktionstyp" in transaction and "meddelande" in transaction:
                kategorisera_transaktion(transaction, kategorier)
            else:
                click.echo(
                    f"Transaktion saknar nödvändiga fält och hoppar över: {transaction}"
                )

        # Spara nya kategorier
        spara_kategorier(kategorier)
        # Spara transaktioner till JSON
        save_to_json(transactions)
        click.echo("Transaktioner har kategoriserats och sparats.")


@cli.command(name="categorize")
@click.option(
    "--file",
    required=True,
    type=click.Path(exists=True),
    help="Path to transaction JSON file",
)
def categorize_cmd(file):
    """Kategorisera transaktioner i en JSON-fil och uppdatera kategorier."""
    transactions_path = Path(file)
    with open(transactions_path, "r", encoding="utf-8") as f:
        transactions = json.load(f)

    kategorier = ladda_kategorier()

    for transaction in transactions:
        if "transaktionstyp" in transaction and "meddelande" in transaction:
            kategorisera_transaktion(transaction, kategorier)
        else:
            click.echo(f"⚠️ Transaktion saknar fält och hoppas över: {transaction}")

    spara_kategorier(kategorier)
    save_to_json(transactions)
    click.echo(f"✅ Kategorisering klar för {file}")


@cli.command(name="set-budget")
@click.option(
    "--file",
    required=True,
    type=click.Path(exists=True),
    help="Path to transaction JSON file",
)
def set_budget_cmd(file):
    """Skapa eller uppdatera budget för en månad baserat på transaktionsfil (inkl. inkomst)."""
    from app.budget.budget_input import create_monthly_budget

    create_monthly_budget(Path(file))


@cli.command()
@click.option(
    "--file", required=True, type=click.Path(exists=True), help="Path to JSON file"
)
@click.option(
    "--save",
    type=click.Choice(["csv", "markdown", "json"]),
    help="Save report to file.",
)
def report(file, save):
    """Generate a monthly spending summary per category from a JSON transaction file."""
    generate_report(file, export_format=save)


@cli.command(name="report-latest")
@click.option(
    "--save",
    type=click.Choice(["csv", "markdown", "json"]),
    help="Save report to file.",
)
def report_latest(save):
    """Skapa rapport från senaste importerade fil i mappen 'data/'."""
    generate_latest_report(export_format=save)


@cli.command(name="budget-check")
@click.option(
    "--budget-path",
    default=str(BUDGET_PATH),
    type=click.Path(exists=True),
    help="Path to the budget.json file",
)
@click.option(
    "--transactions-path",
    default=None,
    type=click.Path(exists=True),
    help="Path to transactions JSON (latest import). If not provided, auto-detect latest.",
)
def budget_check_cmd(budget_path, transactions_path):
    """
    Check if your spending exceeds the monthly budget limits.
    """
    budget_file = Path(budget_path)

    if transactions_path:
        transactions_file = Path(transactions_path)
    else:
        # Försök hitta senaste importfil i mappen data/
        json_files = sorted(DATA_DIR.glob("import_*.json"), reverse=True)
        if not json_files:
            click.echo("❌ No import files found in data/.")
            return
        transactions_file = json_files[0]

    check_budget(budget_file, transactions_file)


if __name__ == "__main__":
    cli()
