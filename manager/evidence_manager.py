from datetime import datetime

from collector.registry import USBRegistryCollector
from collector.mounteddevices import MountedDevicesCollector
from database.database import EvidenceDatabase
from reports.case_report import CaseReport
from reports.pdf_report import PDFReport
from utils.hash_utils import HashUtils
from reports.case_export import CaseExport

class EvidenceManager:

    def __init__(self):

        self.registry = USBRegistryCollector()
        self.mounted_collector = MountedDevicesCollector()
        self.database = EvidenceDatabase()

        self.case_id = self.database.create_case(
            "USB Investigation Case 001",
            "Analyst"
        )

    # -------------------------
    # TIMELINE
    # -------------------------
    def add_timeline(self, artifact, description):

        event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        record_hash = HashUtils.sha256({
            "time": event_time,
            "artifact": artifact,
            "description": description
        })

        self.database.insert_timeline_event(
            event_time,
            artifact,
            description,
            record_hash
        )

    # -------------------------
    # CORRELATION
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
                        f"{device.serial_number} → {mount.drive_letter} ({score}%)"
                    )

        return correlations

    # -------------------------
    # MAIN PIPELINE
    # -------------------------
    def collect(self):

        devices = self.registry.collect()

        for device in devices:

            record_hash = HashUtils.sha256(device.__dict__)

            self.database.insert_device(device, self.case_id, record_hash)

            self.add_timeline(
                "USB_DEVICE",
                f"Detected {device.product}"
            )

        mounted = self.mounted_collector.collect()

        for item in mounted:

            record_hash = HashUtils.sha256(item.__dict__)

            self.database.insert_mounted_device(item, self.case_id, record_hash)

            self.add_timeline(
                "MOUNTED_DEVICE",
                f"Detected {item.drive_letter}"
            )

        correlations = self.correlate(devices, mounted)
        timeline = self.database.get_timeline()

        CaseReport.generate(
            self.database.get_latest_case(),
            devices,
            mounted,
            correlations,
            timeline
        )

        PDFReport.generate(
            self.database.get_latest_case(),
            devices,
            mounted,
            correlations,
            timeline
        )

        return devices, mounted, correlations, timeline

    # -------------------------
    # QUERY
    # -------------------------
    def query_device(self, serial):

        device = self.database.get_device_by_serial(serial)
        timeline = self.database.get_timeline()

        return device, timeline
    
    def export_case(self):

        case = self.database.get_latest_case()

        if case:
            CaseExport.export(case[0])
        else:
            print("No case found")

    # -------------------------
    # CLOSE
    # -------------------------
    def close(self):
        self.database.close()