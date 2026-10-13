"""LocalQuant 数据库自动化测试。"""

import sqlite3
import tempfile
import unittest
from pathlib import Path

from src.database import connect_db, get_table_names, initialize_database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_localquant.db"
        initialize_database(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_all_expected_tables_exist(self):
        tables = get_table_names(self.db_path)
        expected = {
            "assets",
            "market_prices",
            "portfolio_snapshots",
            "cash_flows",
            "decision_logs",
            "backtest_runs",
        }
        self.assertTrue(expected.issubset(set(tables)))

    def test_can_insert_and_read_asset(self):
        with connect_db(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO assets (symbol, name, asset_type, market, currency)
                VALUES (?, ?, ?, ?, ?)
                """,
                ("DEMO_CN", "模拟中国资产", "index_fund", "CN", "CNY"),
            )
            row = connection.execute(
                "SELECT symbol, name, market, currency FROM assets WHERE symbol = ?",
                ("DEMO_CN",),
            ).fetchone()

        self.assertIsNotNone(row)
        self.assertEqual(row["symbol"], "DEMO_CN")
        self.assertEqual(row["market"], "CN")
        self.assertEqual(row["currency"], "CNY")

    def test_duplicate_asset_symbol_is_rejected(self):
        with connect_db(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO assets (symbol, name, asset_type, market, currency)
                VALUES (?, ?, ?, ?, ?)
                """,
                ("DEMO_US", "Demo US Asset", "etf", "US", "USD"),
            )
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    """
                    INSERT INTO assets (symbol, name, asset_type, market, currency)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    ("DEMO_US", "Duplicate", "etf", "US", "USD"),
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
