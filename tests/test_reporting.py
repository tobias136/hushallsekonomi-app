import unittest
from app.reports.reporting import group_by_month_and_category


class TestReporting(unittest.TestCase):
    def test_group_by_month_and_category(self):
        transactions = [
            {"date": "2025-04-15", "amount": "100.00", "category": "needs"},
            {"date": "2025-04-20", "amount": "50.00", "category": "wants"},
            {"date": "2025-05-01", "amount": "200.00", "category": "needs"},
            {"date": "2025-05-15", "amount": "300.00", "category": "wants"},
            {"date": "2025-05-20", "amount": "25.00", "category": "needs"},
        ]

        result = group_by_month_and_category(transactions)

        self.assertEqual(result["2025-04"]["needs"], 100.00)
        self.assertEqual(result["2025-04"]["wants"], 50.00)
        self.assertEqual(result["2025-05"]["needs"], 225.00)
        self.assertEqual(result["2025-05"]["wants"], 300.00)
