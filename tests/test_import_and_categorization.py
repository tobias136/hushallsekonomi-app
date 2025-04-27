# tests/test_import_and_categorization.py

import pytest
from scripts.import_transactions import import_csv
from app.categorizer.kategorisering import (
    ladda_kategorier,
    spara_kategorier,
    kategorisera_transaktion,
)


@pytest.fixture
def sample_csv(tmp_path):
    # Skapa en tillfällig testfil
    content = (
        '"Bokföringsdatum";"Transaktionsdatum";"Transaktionstyp";"Meddelande";"Belopp"\n'
        '"2024-02-02";"2024-02-02";"Kortköp";"Amazon Prime,www.amazon.se,LU";"-59,00"\n'
        '"2024-02-02";"2024-02-01";"Swish till";"Håkan Universeum";"-450,00"\n'
    )
    filepath = tmp_path / "test.csv"
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


def test_import_csv(sample_csv):
    transactions = import_csv(sample_csv)
    assert len(transactions) == 2
    assert all("transaktionstyp" in t for t in transactions)
    assert all("meddelande" in t for t in transactions)


def test_categorization_flow(tmp_path, sample_csv):
    transactions = import_csv(sample_csv)
    kategorier = {}

    # Simulerar att vi väljer 'wants' på alla promptar (mockar input)
    input_values = ["wants", "needs"]

    def mock_input(prompt):
        return input_values.pop(0)

    original_input = __builtins__.input
    __builtins__.input = mock_input

    try:
        for t in transactions:
            kategorisera_transaktion(t, kategorier)
    finally:
        __builtins__.input = original_input  # Säkerställer återställning av input

    assert len(kategorier) == 2
    assert all(t.get("kategori") in ["wants", "needs"] for t in transactions)

    # Testa att spara och ladda kategorier
    kategorier_path = tmp_path / "kategorier.json"
    spara_kategorier(kategorier, kategorier_path)
    loaded_kategorier = ladda_kategorier(kategorier_path)
    assert loaded_kategorier == kategorier
