from datetime import datetime

from collector.registry import USBRegistryCollector
from collector.mounteddevices import MountedDevicesCollector
from database.database import EvidenceDatabase
from reports.json_report import JSONReport


class EvidenceManager:

    def __init__(self):

        self.registry = USBRegistryCollector()
        self.database = EvidenceDatabase()
        self.mounted = MountedDevicesCollector()

    def add_timeline(self, artifact, description):

        event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.database.insert_timeline_event(
            event_time,
            artifact,
            description
        )
    
    def correlate(self, devices, mounted):

        correlations = []

        for device in devices:

            for mount in mounted:

            # SIMPLE heuristic match (baseline forensic linking)
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
    
    def build_timeline_report(self):

        rows = self.database.get_timeline()

        timeline = []

        for row in rows:

            timeline.append({
                "event_time": row[0],
                "artifact": row[1],
                "description": row[2]
        })

        return timeline
    
    def query_device(self, serial_number):

        device = self.database.get_device_by_serial(serial_number)
        timeline = self.database.get_timeline_by_artifact("USB_DEVICE")

        return device, timeline
    
    def full_analysis(self):

        return {
            "devices": self.database.get_all_devices(),
            "mounted": self.database.get_all_mounted(),
            "timeline": self.database.get_timeline()
        }
    
    def collect(self):

        # -------------------------
        # USB Registry Collection
        # -------------------------
        devices = self.registry.collect()

        for device in devices:

            self.database.insert_device(device)

            self.add_timeline(
                "USB_DEVICE",
                f"USB detected: {device.product} ({device.serial_number})"
            )

        # -------------------------
        # Mounted Devices Collection
        # -------------------------
        mounted = self.mounted.collect()

        for item in mounted:

            self.database.insert_mounted_device(item)

            self.add_timeline(
                "MOUNTED_DEVICE",
                f"Drive detected: {item.drive_letter}"
            )

        # -------------------------
        # JSON Report (USB only)
        # -------------------------
        JSONReport.save(devices)

        correlations = self.correlate(devices, mounted)
        timeline = self.build_timeline_report()

        return devices, mounted, correlations, timeline
    

    def close(self):

        self.database.close()