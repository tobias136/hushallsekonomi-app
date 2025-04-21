import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from scripts.import_transactions import import_csv, save_to_json


import click
from scripts.import_transactions import import_csv

@click.group()
def cli():
    """Hushållsekonomi CLI-verktyg."""
    pass

@cli.command()
@click.argument('filnamn', type=click.Path(exists=True))
def importera(filnamn):
    """Importera transaktioner från en CSV-fil."""
    click.echo(f"Importerar från {filnamn}...")
    transactions = import_csv(filnamn)
    click.echo(f"{len(transactions)} transaktioner importerade.")
    if transactions:
        save_to_json(transactions)


if __name__ == '__main__':
    cli()
