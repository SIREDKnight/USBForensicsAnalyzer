import sqlite3
from pathlib import Path


DB_FILE = Path("database") / "evidence.db"



class EvidenceDatabase:


    def __init__(self):

        DB_FILE.parent.mkdir(
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            DB_FILE
        )

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        self.create_tables()



    # =====================================================
    # TABLE CREATION
    # =====================================================

    def create_tables(self):


        self.cursor.execute("""
        
        CREATE TABLE IF NOT EXISTS cases(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            case_id TEXT UNIQUE,

            case_name TEXT,

            created_at TEXT,

            investigator TEXT

        )

        """)



        self.cursor.execute("""
        
        CREATE TABLE IF NOT EXISTS usb_devices(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            manufacturer TEXT,

            product TEXT,

            revision TEXT,

            serial_number TEXT UNIQUE,

            registry_path TEXT,

            case_id INTEGER,

            hash TEXT

        )

        """)



        self.cursor.execute("""
        
        CREATE TABLE IF NOT EXISTS mounted_devices(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            drive_letter TEXT,

            registry_name TEXT,

            volume_guid TEXT,

            case_id INTEGER,

            hash TEXT

        )

        """)



        self.cursor.execute("""
        
        CREATE TABLE IF NOT EXISTS event_logs(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            event_id INTEGER,

            source TEXT,

            timestamp TEXT,

            description TEXT,

            hash TEXT

        )

        """)



        self.cursor.execute("""
        
        CREATE TABLE IF NOT EXISTS timeline(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            event_time TEXT,

            artifact TEXT,

            description TEXT,

            hash TEXT

        )

        """)



        self.connection.commit()



    # =====================================================
    # CASE MANAGEMENT
    # =====================================================


    def create_case(

            self,

            case_id,

            case_name,

            investigator):


        self.cursor.execute("""

        INSERT INTO cases(

            case_id,

            case_name,

            created_at,

            investigator

        )

        VALUES(

            ?,

            ?,

            datetime('now'),

            ?

        )

        """,

        (

            case_id,

            case_name,

            investigator

        ))



        self.connection.commit()


        return self.cursor.lastrowid



    def get_latest_case(self):


        self.cursor.execute("""

        SELECT *

        FROM cases

        ORDER BY id DESC

        LIMIT 1

        """)


        return self.cursor.fetchone()



    # =====================================================
    # USB DEVICES
    # =====================================================


    def insert_device(

            self,

            device,

            case_id,

            record_hash):


        self.cursor.execute("""

        INSERT OR IGNORE INTO usb_devices(

            manufacturer,

            product,

            revision,

            serial_number,

            registry_path,

            case_id,

            hash

        )

        VALUES(?,?,?,?,?,?,?)

        """,

        (

            device.manufacturer,

            device.product,

            device.revision,

            device.serial_number,

            device.registry_path,

            case_id,

            record_hash

        ))



        self.connection.commit()



    # =====================================================
    # MOUNTED DEVICES
    # =====================================================


    def insert_mounted_device(

            self,

            mounted,

            case_id,

            record_hash):


        self.cursor.execute("""

        INSERT INTO mounted_devices(

            drive_letter,

            registry_name,

            volume_guid,

            case_id,

            hash

        )

        VALUES(?,?,?,?,?)

        """,

        (

            mounted.drive_letter,

            mounted.registry_name,

            mounted.volume_guid,

            case_id,

            record_hash

        ))



        self.connection.commit()



    # =====================================================
    # EVENT LOGS
    # =====================================================


    def insert_event_log(

            self,

            event_id,

            source,

            timestamp,

            description,

            record_hash=None):


        self.cursor.execute("""

        INSERT INTO event_logs(

            event_id,

            source,

            timestamp,

            description,

            hash

        )

        VALUES(?,?,?,?,?)

        """,

        (

            event_id,

            source,

            timestamp,

            description,

            record_hash

        ))



        self.connection.commit()



    # =====================================================
    # TIMELINE
    # =====================================================


    def insert_timeline_event(

            self,

            event_time,

            artifact,

            description,

            record_hash):


        self.cursor.execute("""

        INSERT INTO timeline(

            event_time,

            artifact,

            description,

            hash

        )

        VALUES(?,?,?,?)

        """,

        (

            event_time,

            artifact,

            description,

            record_hash

        ))



        self.connection.commit()



    def get_timeline(self):


        self.cursor.execute("""

        SELECT

            event_time,

            artifact,

            description

        FROM timeline

        ORDER BY event_time

        """)


        return self.cursor.fetchall()



    # =====================================================
    # SEARCH
    # =====================================================


    def get_device_by_serial(

            self,

            serial):


        self.cursor.execute("""

        SELECT *

        FROM usb_devices

        WHERE serial_number=?

        """,

        (

            serial,

        ))


        return self.cursor.fetchone()



    # =====================================================
    # CLOSE
    # =====================================================


    def close(self):

        self.connection.close()