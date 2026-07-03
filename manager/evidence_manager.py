from datetime import datetime
import hashlib

from collector.registry import USBRegistryCollector
from collector.mounteddevices import MountedDevicesCollector
from database.database import EvidenceDatabase
from reports.case_report import CaseReport


class EvidenceManager:

    def __init__(self):

        self.registry = USBRegistryCollector()
        self.mounted_collector = MountedDevicesCollector()
        self.database = EvidenceDatabase()

        # -------------------------
        # CREATE CASE
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
    # HASH (for future integrity use)
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

                score = 0

                if device.serial_number in mount.registry_name:
                    score += 60

                if device.product.lower() in mount.registry_name.lower():
                    score += 20

                if "USB" in mount.registry_name.upper():
                    score += 10

                if score >= 60:

                    correlations.append({
                        "serial_number": device.serial_number,
                        "drive_letter": mount.drive_letter,
                        "product": device.product,
                        "confidence": score
                    })

                    self.add_timeline(
                        "CORRELATION",
                        f"{device.serial_number} linked to {mount.drive_letter} ({score}%)"
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
                f"Detected USB: {device.product} ({device.serial_number})"
            )

        # MOUNTED DEVICES
        mounted = self.mounted_collector.collect()

        for item in mounted:

            self.database.insert_mounted_device(item, self.case_id)

            self.add_timeline(
                "MOUNTED_DEVICE",
                f"Detected mount: {item.drive_letter}"
            )

        # CORRELATIONS
        correlations = self.correlate(devices, mounted)

        # TIMELINE FETCH
        timeline = self.database.get_timeline()

        # -------------------------
        # GENERATE FORENSIC REPORT
        # -------------------------
        CaseReport.generate(
            self.database.get_latest_case(),
            devices,
            mounted,
            correlations,
            timeline
        )

        return devices, mounted, correlations, timeline

    # -------------------------
    # QUERY ENGINE
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