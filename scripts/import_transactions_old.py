import sys
import os
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app.database import Database

VALID_CATEGORIES = ["wants", "needs", "necessities", "savings"]

def clean_amount(amount_str):
    # Byt ut mellanslag och komma mot punkt för att kunna göra float
    cleaned = amount_str.replace(" ", "").replace(",", ".")
    return float(cleaned)

def prompt_for_category(description):
    """Fråga användaren om kategori för en ny beskrivning.
    Args: description (str): Beskrivning av transaktionen som saknar kategori.
    Returns: str: Den valda kategorin från VALID_CATEGORIES.
    """
    print(f"\nNy beskrivning upptäckt: '{description}'")
    print("Välj en kategori:")
    for i, cat in enumerate(VALID_CATEGORIES, start=1):
        print(f"{i}. {cat}")

    while True:
        try:
            choice = input("Ange siffra för kategori: ")
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(VALID_CATEGORIES):
                    return VALID_CATEGORIES[choice - 1]
            print("Ogiltigt val. Försök igen.")
        except KeyboardInterrupt:
            print("Användern avbröt inmatningen.")
            return None

def import_transactions_from_csv(csv_file):
    db = Database()
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';', quotechar='"')

            # Hoppa över kontoinformation (2 rader med saldo etc.)
            next(reader)  # "Kontonummer";"Kontonamn";...
            next(reader)  # "2342342342";"Lönekonto";...

            # Ev. tom rad – om din fil inte har en extra tom rad, kommentera ut raden nedan
            empty_line = next(reader)

            # Rubrikrad för transaktioner:
            header = next(reader)
            # header ex: ["Bokföringsdatum", "Transaktionsdatum", "Transaktionstyp", "Meddelande", "Belopp"]

            count_imported = 0

            for row in reader:
                if len(row) < 5:
                    # Tom eller ofullständig rad
                    continue

                booking_date = row[0]       # "2024-11-29"
                transaction_date = row[1]   # "2024-11-29"
                transaction_type = row[2]   # "Kortköp"
                message = row[3]            # ex: "GOOGLE *Google One..."
                amount_str = row[4]         # ex: "-19,00"

                # Försök rensa och konvertera beloppet
                try:
                    amount = clean_amount(amount_str)
                except ValueError:
                    print(f"Ogiltigt belopp på raden: {row}")
                    continue

                # Kolla om beskrivningen är känd
                known_cat = db.get_category_for_description(message)
                if known_cat is None:
                    # Ingen känd kategori, fråga användaren
                    category = prompt_for_category(message)
                    db.add_known_category(message, category)
                else:
                    category = known_cat

                # Lägg till transaktionen
                trans_id = db.add_transaction(transaction_date, amount, message, category)
                count_imported += 1

                print(f"Importerat transaktion {trans_id} (beskrivning: {message}) med kategori '{category}'.")
    finally:
        db.close()
        print(f"\nTotalt importerade transaktioner: {count_imported}")

if __name__ == "__main__":
    # Fråga användaren om datum för CSV-filen
    date_input = input("Ange datum (YYYY-MM-DD) för CSV-filen du vill läsa in: ")
    # Bygg filnamnet utifrån datumet
    # ex: "../csv/Lönekonto 2024-11-30.csv"
    csv_file_path = os.path.join(BASE_DIR, "csv", f"Lönekonto {date_input}.csv")

    if not os.path.exists(csv_file_path):
        print(f"Filen '{csv_file_path}' existerar inte. Kontrollera datum eller filnamn.")
        sys.exit(1)

    import_transactions_from_csv(csv_file_path)
