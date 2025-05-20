# app/CLI/main.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import click
from scripts.import_transactions import import_csv, save_to_json
from app.categorizer.kategorisering import (
    ladda_kategorier,
    spara_kategorier,
    kategorisera_transaktion,
)
from app.reports.reporting import generate_report


@click.group()
def cli():
    """Hushållsekonomi CLI-verktyg."""
    pass


@cli.command()
@click.argument("filnamn", type=click.Path(exists=True))
def importera(filnamn):
    """Importera transaktioner från en CSV-fil och kategorisera dem."""
    click.echo(f"Importerar från {filnamn}...")

    # Importera transaktioner
    transactions = import_csv(filnamn)
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


@cli.command()
@click.argument("filepath", type=click.Path(exists=True))
def report(filepath):
    """Generate a monthly spending summary per category from a JSON transaction file."""
    generate_report(filepath)


if __name__ == "__main__":
    cli()
