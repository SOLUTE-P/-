"""LocalQuant SQLite 数据库基础设施。"""

import sqlite3
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "localquant.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS assets (
    asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    asset_type TEXT NOT NULL,
    market TEXT NOT NULL,
    currency TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS market_prices (
    price_id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    price_date TEXT NOT NULL,
    price REAL NOT NULL CHECK (price > 0),
    price_type TEXT NOT NULL DEFAULT 'close',
    source TEXT NOT NULL,
    fetched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (asset_id, price_date, price_type, source),
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);

CREATE TABLE IF NOT EXISTS portfolio_snapshots (
    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_date TEXT NOT NULL,
    asset_id INTEGER NOT NULL,
    quantity REAL NOT NULL CHECK (quantity >= 0),
    market_value REAL NOT NULL CHECK (market_value >= 0),
    currency TEXT NOT NULL,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);

CREATE TABLE IF NOT EXISTS cash_flows (
    cash_flow_id INTEGER PRIMARY KEY AUTOINCREMENT,
    flow_date TEXT NOT NULL,
    flow_type TEXT NOT NULL,
    amount REAL NOT NULL,
    currency TEXT NOT NULL,
    note TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS decision_logs (
    decision_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    asset_id INTEGER,
    strategy_type TEXT NOT NULL,
    action TEXT NOT NULL,
    rationale TEXT NOT NULL,
    risk_flags TEXT,
    confidence REAL,
    status TEXT NOT NULL DEFAULT 'pending',
    requires_confirmation INTEGER NOT NULL DEFAULT 1 CHECK (requires_confirmation IN (0, 1)),
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);

CREATE TABLE IF NOT EXISTS backtest_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_name TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    initial_capital REAL NOT NULL CHECK (initial_capital >= 0),
    total_return REAL,
    max_drawdown REAL,
    sharpe_ratio REAL,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def connect_db(db_path: str | Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """打开数据库连接，并启用外键约束。"""
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(db_path: str | Path = DEFAULT_DB_PATH) -> Path:
    """创建所有初始表；重复运行不会重复创建表或删除数据。"""
    path = Path(db_path)
    with connect_db(path) as connection:
        connection.executescript(SCHEMA)
    return path


def get_table_names(db_path: str | Path = DEFAULT_DB_PATH) -> list[str]:
    """返回当前数据库中的用户表名称。"""
    with connect_db(db_path) as connection:
        rows: Iterable[sqlite3.Row] = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()
    return [row["name"] for row in rows]
