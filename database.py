

import sqlite3
from pathlib import Path


DEFAULT_DB_PATH = Path(__file__).resolve().parent / "countries.db"


class CountryDatabaseManager:
    """Owns the SQLite connection and CRUD operations for country records."""

    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = str(db_path)
        self.create_table()

    def _connect(self):
        """Open a database connection that returns rows by column name."""
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def create_table(self):
        """Create the countries table if it does not already exist."""
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS countries (
                    country_name TEXT PRIMARY KEY,
                    capital TEXT NOT NULL,
                    population INTEGER NOT NULL,
                    area REAL NOT NULL
                )
                """
            )

    @staticmethod
    def _row_to_dict(row):
        """Convert one SQLite row to a regular Python dictionary."""
        return dict(row) if row is not None else None

    def create_country(self, country):
        """Insert a country. Returns False if its name already exists."""
        try:
            with self._connect() as connection:
                connection.execute(
                    """
                    INSERT INTO countries (country_name, capital, population, area)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        country["country_name"],
                        country["capital"],
                        int(country["population"]),
                        float(country["area"]),
                    ),
                )
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all_countries(self):
        """Return every country as a list of dictionaries."""
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT country_name, capital, population, area
                FROM countries
                ORDER BY country_name
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def get_country(self, country_name):
        """Return one country by its name, or None when it is missing."""
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT country_name, capital, population, area
                FROM countries
                WHERE country_name = ?
                """,
                (country_name,),
            ).fetchone()
        return self._row_to_dict(row)

    def update_country(self, country_name, country):
        """Update an existing country. Returns True if a row was changed."""
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE countries
                SET capital = ?, population = ?, area = ?
                WHERE country_name = ?
                """,
                (
                    country["capital"],
                    int(country["population"]),
                    float(country["area"]),
                    country_name,
                ),
            )
        return cursor.rowcount > 0

    def delete_country(self, country_name):
        """Delete a country. Returns True if a row was deleted."""
        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM countries WHERE country_name = ?",
                (country_name,),
            )
        return cursor.rowcount > 0
