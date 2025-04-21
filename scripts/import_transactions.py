import pandas as pd
import os
import json
from datetime import datetime

def import_csv(filnamn: str):
    """
    Importerar transaktioner från CSV med metainfo före datan.
    Hanterar tusentalsavgränsare och olika datumformat.
    """
    try:
        with open(filnamn, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        start_line = None
        for i, line in enumerate(lines):
            if 'Transaktionsdatum' in line:
                start_line = i
                break

        if start_line is None:
            print("Kunde inte hitta rubrikraden med 'Transaktionsdatum'.")
            return []

        df = pd.read_csv(filnamn, sep=';', skiprows=start_line, on_bad_lines='skip')
        df.columns = df.columns.str.strip().str.strip('"')

        print("Kolumner i transaktionsdelen:", list(df.columns))  # Debug

        df = df.rename(columns={
            'Transaktionsdatum': 'datum',
            'Transaktionstyp': 'beskrivning',
            'Belopp': 'belopp'
        })

        df['datum'] = pd.to_datetime(df['datum'], errors='coerce')

        # Ta bort mellanslag + byt komma till punkt → konvertera till float
        df['belopp'] = (
            df['belopp']
            .astype(str)
            .str.replace(' ', '', regex=False)
            .str.replace(',', '.', regex=False)
            .astype(float)
        )

        transactions = df[['datum', 'beskrivning', 'belopp']].dropna().to_dict(orient='records')

        print("Förhandsgranskning:")
        for t in transactions[:5]:
            print(t)

        return transactions

    except Exception as e:
        print(f"Fel vid import: {e}")
        return []


def save_to_json(transactions, export_dir='data'):
    """
    Sparar transaktioner till en .json-fil, med datumen som ISO-strängar.
    """
    if not transactions:
        print("Inga transaktioner att spara.")
        return

    # Konvertera datum till ISO-format (YYYY-MM-DD)
    for t in transactions:
        if isinstance(t['datum'], pd.Timestamp):
            t['datum'] = t['datum'].date().isoformat()

    os.makedirs(export_dir, exist_ok=True)
    datum_str = datetime.now().strftime('%Y-%m-%d')
    export_path = os.path.join(export_dir, f"import_{datum_str}.json")

    try:
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(transactions, f, ensure_ascii=False, indent=2)
        print(f"Transaktioner sparade till: {export_path}")
    except Exception as e:
        print(f"Fel vid export till JSON: {e}")
