import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.expanduser("~/.local/share/netsen/netsen.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                date    TEXT NOT NULL,
                network TEXT NOT NULL,
                total   INTEGER NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS hosts (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER NOT NULL,
                ip      TEXT NOT NULL,
                mac     TEXT,
                vendor  TEXT,
                ports   TEXT,
                FOREIGN KEY (scan_id) REFERENCES scans(id)
            )
        """)


def save_scan(data: list, network: str):
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO scans (date, network, total) VALUES (?, ?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), network, len(data))
        )
        scan_id = cursor.lastrowid

        for host in data:
            ports_str = ",".join(map(str, host["ports"]))
            conn.execute(
                "INSERT INTO hosts (scan_id, ip, mac, vendor, ports) VALUES (?, ?, ?, ?, ?)",
                (scan_id, host["ip"], host["mac"], host["vendor"], ports_str)
            )

def get_history():
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT * FROM scans ORDER BY id DESC"
        )
        return cursor.fetchall()


def get_scan_detail(scan_id: int):
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT * FROM hosts WHERE scan_id = ?", (scan_id,)
        )
        return cursor.fetchall()





















