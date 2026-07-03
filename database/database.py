import sqlite3
from pathlib import Path

DB_FILE = Path("database") / "evidence.db"


class EvidenceDatabase:

    def __init__(self):
        self.connection = sqlite3.connect(DB_FILE)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usb_devices (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                manufacturer TEXT,

                product TEXT,

                revision TEXT,

                serial_number TEXT UNIQUE,

                registry_path TEXT

            )
        """)

        self.connection.commit()

    def insert_device(self, device):

        self.cursor.execute("""

            INSERT OR IGNORE INTO usb_devices(

                manufacturer,
                product,
                revision,
                serial_number,
                registry_path

            )

            VALUES (?, ?, ?, ?, ?)

        """,

        (

            device.manufacturer,
            device.product,
            device.revision,
            device.serial_number,
            device.registry_path

        ))

        self.connection.commit()

    def close(self):

        self.connection.close()