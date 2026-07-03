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

     self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS mounted_devices (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            drive_letter TEXT,

            volume_guid TEXT,

            registry_name TEXT
        )
    """)

     self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS event_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            event_id INTEGER,

            source TEXT,

            timestamp TEXT,

            description TEXT
        )
    """)

     self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS timeline (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            event_time TEXT,

            artifact TEXT,

            description TEXT
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

    def insert_mounted_device(self, mounted):

     self.cursor.execute("""

        INSERT INTO mounted_devices(

            drive_letter,
            registry_name

        )

        VALUES (?, ?)

    """,

    (

        mounted.drive_letter,
        mounted.registry_name

    ))

     self.connection.commit()

    def insert_timeline_event(self, event_time, artifact, description):

     self.cursor.execute("""
        INSERT INTO timeline (
            event_time,
            artifact,
            description
        )
        VALUES (?, ?, ?)
    """,
    (
        event_time,
        artifact,
        description
    ))

     self.connection.commit()

    def get_timeline(self):

     self.cursor.execute("""
        SELECT event_time, artifact, description
        FROM timeline
        ORDER BY event_time ASC
    """)

     return self.cursor.fetchall() 
    
    def get_all_devices(self):

        self.cursor.execute("""
        SELECT manufacturer, product, revision, serial_number, registry_path
        FROM usb_devices
        """)

        return self.cursor.fetchall()
    
    def get_device_by_serial(self, serial):

        self.cursor.execute("""
        SELECT manufacturer, product, revision, serial_number, registry_path
        FROM usb_devices
        WHERE serial_number = ?
        """, (serial,))

        return self.cursor.fetchone()
    
    def get_all_mounted(self):

        self.cursor.execute("""
        SELECT drive_letter, registry_name
        FROM mounted_devices
        """)

        return self.cursor.fetchall()
    
    def get_timeline_by_artifact(self, artifact):

        self.cursor.execute("""
        SELECT event_time, artifact, description
        FROM timeline
        WHERE artifact = ?
        ORDER BY event_time
        """, (artifact,))

        return self.cursor.fetchall()

    def close(self):

        self.connection.close()