import unittest
from unittest.mock import patch, mock_open
from scripts.import_transactions import import_transactions_from_csv, clean_amount, prompt_for_category
import io

class TestImportTransactions(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data=(
        '"Kontonummer";"Kontonamn";"";"Saldo";"Tillgängligt belopp"\n'
        '"2342342342";"Lönekonto";"";"10 243,72";"10 243,72"\n'
        '\n'
        '"Bokföringsdatum";"Transaktionsdatum";"Transaktionstyp";"Meddelande";"Belopp"\n'
        '"2024-11-29";"2024-11-29";"Kortköp";"GOOGLE *Google One,650-253-0000,IE";"-19,00"\n'
    ))
    @patch('scripts.import_transactions.Database')
    def test_import_transactions_from_csv(self, mock_database, mock_file):
        # Setup
        db_instance = mock_database.return_value
        db_instance.get_category_for_description.return_value = None
        with patch('scripts.import_transactions.prompt_for_category', return_value='wants') as mock_prompt:
            # Act
            import_transactions_from_csv('fakefile.csv')

            # Assert
            # Kontrollera att filen öppnades korrekt
            mock_file.assert_called_with('fakefile.csv', 'r', encoding='utf-8')
            # Kontrollera att prompt_for_category anropades korrekt
            mock_prompt.assert_called_once_with('GOOGLE *Google One,650-253-0000,IE')
            # Kontrollera att transaktionerna läggs till korrekt
            db_instance.add_transaction.assert_called_once_with(
                '2024-11-29', -19.00, 'GOOGLE *Google One,650-253-0000,IE', 'wants'
            )
            # Kontrollera att databasen stängs
            db_instance.close.assert_called_once()

    def test_clean_amount(self):
        # Testa att rensa belopp
        result = clean_amount("-1 750,00")
        self.assertEqual(result, -1750.00)

    @patch('builtins.input', side_effect=['3'])
    def test_prompt_for_category(self, mock_input):
        # Testa att prompt for category returnerar rätt kategori
        result = prompt_for_category('description')
        self.assertEqual(result, 'necessities')

if __name__ == '__main__':
    unittest.main()
