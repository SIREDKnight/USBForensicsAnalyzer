from datetime import datetime
import hashlib

from collector.registry import USBRegistryCollector
from collector.mounteddevices import MountedDevicesCollector
from database.database import EvidenceDatabase
from reports.json_report import JSONReport


class EvidenceManager:

    def __init__(self):

        self.registry = USBRegistryCollector()
        self.database = EvidenceDatabase()
        self.mounted = MountedDevicesCollector()

        # -------------------------
        # FORENSIC CASE CREATION
        # -------------------------
        self.case_id = self.database.create_case(
            "USB Investigation Case 001",
            "Analyst"
        )

    # -------------------------
    # TIMELINE LOGGER
    # -------------------------
    def add_timeline(self, artifact, description):

        event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.database.insert_timeline_event(
            event_time,
            artifact,
            description
        )

    # -------------------------
    # HASH FUNCTION (FORENSIC INTEGRITY READY)
    # -------------------------
    def generate_hash(self, data):

        return hashlib.sha256(str(data).encode()).hexdigest()

    # -------------------------
    # CORRELATION ENGINE
    # -------------------------
    def correlate(self, devices, mounted):

        correlations = []

        for device in devices:

            for mount in mounted:

                # basic heuristic match (can be improved later)
                if device.serial_number[:6] in mount.registry_name:

                    correlations.append({
                        "serial_number": device.serial_number,
                        "drive_letter": mount.drive_letter,
                        "product": device.product
                    })

                    self.add_timeline(
                        "CORRELATION",
                        f"{device.serial_number} linked to {mount.drive_letter}"
                    )

        return correlations

    # -------------------------
    # MAIN COLLECTION PIPELINE
    # -------------------------
    def collect(self):

        # USB DEVICES
        devices = self.registry.collect()

        for device in devices:

            self.database.insert_device(device, self.case_id)

            self.add_timeline(
                "USB_DEVICE",
                f"USB detected: {device.product} ({device.serial_number})"
            )

        # MOUNTED DEVICES
        mounted = self.mounted.collect()

        for item in mounted:

            self.database.insert_mounted_device(item, self.case_id)

            self.add_timeline(
                "MOUNTED_DEVICE",
                f"Drive detected: {item.drive_letter}"
            )

        # CORRELATIONS
        correlations = self.correlate(devices, mounted)

        # FULL TIMELINE OUTPUT
        timeline = self.database.get_timeline()

        return devices, mounted, correlations, timeline

    # -------------------------
    # DEVICE QUERY
    # -------------------------
    def query_device(self, serial_number):

        device = self.database.get_device_by_serial(serial_number)

        timeline = self.database.get_timeline_by_artifact("USB_DEVICE")

        return device, timeline

    # -------------------------
    # CLOSE CONNECTION
    # -------------------------
    def close(self):

        self.database.close()