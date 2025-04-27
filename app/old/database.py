import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "finance_app.db")


class Database:
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self.conn = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Anslut till SQLite-databasen."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = (
            sqlite3.Row
        )  # Gör att resultatet kan hanteras som ett dictionary-liknande objekt.

    def create_tables(self):
        """Skapa nödvändiga tabeller om de inte redan finns."""
        cursor = self.conn.cursor()

        # Skapa transactions-tabell
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                amount REAL,
                description TEXT,
                category TEXT
            )
        """
        )

        # Skapa known_categories-tabell
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS known_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT UNIQUE,
                category TEXT
            )
        """
        )

        self.conn.commit()

    def add_transaction(self, date, amount, description, category=None):
        """
        Lägg till en transaktion i databasen.
        Om category är None, lagras transaktionen utan kategori.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO transactions (date, amount, description, category)
            VALUES (?, ?, ?, ?)
        """,
            (date, amount, description, category),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_transactions(self):
        """Hämta alla transaktioner från databasen."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM transactions")
        return cursor.fetchall()

    def add_known_category(self, description, category):
        """
        Lägg till en känd kategori-koppling.
        Om beskrivningen redan finns, uppdatera kategorin.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO known_categories (description, category)
            VALUES (?, ?)
            ON CONFLICT(description) DO UPDATE SET category=excluded.category
        """,
            (description, category),
        )
        self.conn.commit()

    def get_category_for_description(self, description):
        """
        Hämta kategori för en given beskrivning, om den finns lagrad.
        Returnerar None om ingen känd kategori finns.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT category FROM known_categories WHERE description = ?",
            (description,),
        )
        row = cursor.fetchone()
        return row["category"] if row else None

    def close(self):
        """Stäng anslutningen till databasen."""
        if self.conn:
            self.conn.close()
            self.conn = None
