# kategorisering.py

import json
import os


def ladda_kategorier(filepath="data/kategorier.json"):
    """Ladda sparade kategorier baserat på transaktionstyp och meddelande."""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}


def spara_kategorier(kategorier, filepath="data/kategorier.json"):
    """Spara kategorival till fil."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(kategorier, f, ensure_ascii=False, indent=2)


def kategorisera_transaktion(transaktion, kategorier):
    """
    Kontrollera om transaktionsbeskrivning är kategoriserad baserat på transaktionstyp och meddelande.
    Om inte, prompta användaren att välja kategori.
    """
    # Hämtar transaktionstyp och meddelande från transaktionen
    transaktionstyp = transaktion.get("transaktionstyp", "").strip()
    meddelande = transaktion.get("meddelande", "").strip()

    if not meddelande:
        meddelande = "[ingen information]"

    # Nyckel för kategorisering: kombination av transaktionstyp och meddelande
    nyckel = f"{transaktionstyp} - {meddelande}"

    if nyckel in kategorier:
        # Använd tidigare sparad kategori
        transaktion["kategori"] = kategorier[nyckel]
    else:
        print(f"\nTransaktionstyp: {transaktionstyp}")
        print(f"Meddelande: {meddelande}")
        while True:
            kategori = (
                input("Välj kategori (wants / needs / culture / savings / income): ")
                .strip()
                .lower()
            )
            if kategori in {"wants", "needs", "culture", "savings", "income"}:
                break
            else:
                print("Felaktig inmatning. Försök igen.")

        # Spara användarens val som kategori
        transaktion["kategori"] = kategori
        kategorier[nyckel] = kategori

    return transaktion
