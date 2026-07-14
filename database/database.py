import sqlite3

from utils.app_paths import AppPaths
from datetime import datetime


AppPaths.initialize()


DATABASE_FILE = (
    AppPaths.DATABASE_DIR
    /
    "evidence.db"
)



class EvidenceDatabase:


    def __init__(self):

        self.connection = sqlite3.connect(
            DATABASE_FILE
        )

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        self.create_tables()



    # ==================================================
    # DATABASE STRUCTURE
    # ==================================================

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

            serial_number TEXT,

            registry_path TEXT,

            last_connected TEXT,

            registry_timestamp TEXT,

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

            registry_timestamp TEXT,

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

            case_id INTEGER,

            hash TEXT

        )
        """)



        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS timeline(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            event_time TEXT,

            artifact TEXT,

            event_id INTEGER,

            source TEXT,

            description TEXT,

            hash TEXT,

            case_id INTEGER

        )
        """)


        self.connection.commit()



    # ==================================================
    # CASE MANAGEMENT
    # ==================================================

    def create_case(
        self,
        generated_case_id,
        case_name,
        investigator):


        created_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        self.cursor.execute(

            """
            INSERT INTO cases(

                case_id,
                case_name,
                created_at,
                investigator

            )

            VALUES(?,?,?,?)

            """,

            (

                generated_case_id,

                case_name,

                created_time,

                investigator

            )

        )


        self.connection.commit()


        return self.cursor.lastrowid


    def get_latest_case(self):


        self.cursor.execute(

            """
            SELECT *

            FROM cases

            ORDER BY id DESC

            LIMIT 1

            """

        )


        row = self.cursor.fetchone()


        if row:

            return dict(row)


        return None



    def get_case_by_id(
            self,
            case_id):


        self.cursor.execute(

            """
            SELECT *

            FROM cases

            WHERE id=?

            """,

            (
                case_id,
            )

        )


        row = self.cursor.fetchone()


        if row:

            return dict(row)


        return None



    # ==================================================
    # USB DEVICES
    # ==================================================

    def insert_device(
            self,
            device,
            case_id,
            record_hash):


        self.cursor.execute(

            """
            INSERT INTO usb_devices(

                manufacturer,

                product,

                revision,

                serial_number,

                registry_path,

                last_connected,

                registry_timestamp,

                case_id,

                hash

            )

            VALUES(?,?,?,?,?,?,?,?,?)

            """,

            (

                device.manufacturer,

                device.product,

                device.revision,

                device.serial_number,

                device.registry_path,

                device.last_connected,

                device.registry_timestamp,

                case_id,

                record_hash

            )

        )


        self.connection.commit()



    def get_devices_by_case(
            self,
            case_id):


        self.cursor.execute(

            """
            SELECT *

            FROM usb_devices

            WHERE case_id=?

            """,

            (
                case_id,
            )

        )


        return [

            dict(row)

            for row in self.cursor.fetchall()

        ]



    # ==================================================
    # MOUNTED DEVICES
    # ==================================================

    def insert_mounted_device(
            self,
            mounted,
            case_id,
            record_hash):


        self.cursor.execute(

            """
            INSERT INTO mounted_devices(

                drive_letter,

                registry_name,

                volume_guid,

                registry_timestamp,

                case_id,

                hash

            )

            VALUES(?,?,?,?,?,?)

            """,

            (

                mounted.drive_letter,

                mounted.registry_name,

                mounted.volume_guid,

                mounted.registry_timestamp,

                case_id,

                record_hash

            )

        )


        self.connection.commit()



    def get_mounted_by_case(
            self,
            case_id):


        self.cursor.execute(

            """
            SELECT *

            FROM mounted_devices

            WHERE case_id=?

            """,

            (
                case_id,
            )

        )


        return [

            dict(row)

            for row in self.cursor.fetchall()

        ]



    # ==================================================
    # EVENT LOGS
    # ==================================================

    def insert_event_log(
            self,
            event_id,
            source,
            timestamp,
            description,
            record_hash,
            case_id):


        self.cursor.execute(

            """
            INSERT INTO event_logs(

                event_id,

                source,

                timestamp,

                description,

                case_id,

                hash

            )

            VALUES(?,?,?,?,?,?)

            """,

            (

                event_id,

                source,

                timestamp,

                description,

                case_id,

                record_hash

            )

        )


        self.connection.commit()



    def get_events_by_case(
            self,
            case_id):


        self.cursor.execute(

            """
            SELECT *

            FROM event_logs

            WHERE case_id=?

            """,

            (
                case_id,
            )

        )


        return [

            dict(row)

            for row in self.cursor.fetchall()

        ]



    # ==================================================
    # TIMELINE
    # ==================================================

    def insert_timeline_event(
            self,
            event_time,
            artifact,
            description,
            record_hash,
            event_id=None,
            source=None,
            case_id=None):


        self.cursor.execute(

            """
            INSERT INTO timeline(

                event_time,

                artifact,

                event_id,

                source,

                description,

                hash,

                case_id

            )

            VALUES(?,?,?,?,?,?,?)

            """,

            (

                event_time,

                artifact,

                event_id,

                source,

                description,

                record_hash,

                case_id

            )

        )


        self.connection.commit()



    def get_timeline(self):


        self.cursor.execute(

            """
            SELECT *

            FROM timeline

            ORDER BY event_time

            """

        )


        return [

            dict(row)

            for row in self.cursor.fetchall()

        ]



    def get_case_timeline(
            self,
            case_id):


        self.cursor.execute(

            """
            SELECT *

            FROM timeline

            WHERE case_id=?

            ORDER BY event_time

            """,

            (
                case_id,
            )

        )


        return [

            dict(row)

            for row in self.cursor.fetchall()

        ]



    # ==================================================
    # DEVICE SEARCH
    # ==================================================

    def get_device_by_serial(
            self,
            serial):


        self.cursor.execute(

            """
            SELECT *

            FROM usb_devices

            WHERE serial_number=?

            """,

            (
                serial,
            )

        )


        row = self.cursor.fetchone()


        if row:

            return dict(row)


        return None



    # ==================================================
    # CLOSE
    # ==================================================

    def close(self):

        self.connection.close()