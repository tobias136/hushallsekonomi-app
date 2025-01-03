import unittest
import tempfile
import os
from app.database import Database

class TestDatabaseTempFile(unittest.TestCase):
    def setUp(self):
        # Skapa en temporär fil för databasen
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db_path = self.temp_db.name
        self.temp_db.close()  # Stäng för att SQLite ska kunna använda filen
        self.db = Database(db_path=self.temp_db_path)
    
    def tearDown(self):
        self.db.close()
        os.remove(self.temp_db_path)  # Ta bort filen när testet är klart

    def test_add_and_fetch_transactions(self):
        trans_id = self.db.add_transaction("2024-01-01", -500, "ICA Maxi", None)
        self.assertIsNotNone(trans_id)
        
        transactions = self.db.get_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["description"], "ICA Maxi")

if __name__ == '__main__':
    unittest.main()
