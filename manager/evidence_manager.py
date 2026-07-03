from collector.registry import USBRegistryCollector
from database.database import EvidenceDatabase
from reports.json_report import JSONReport
from collector.mounteddevices import MountedDevicesCollector


class EvidenceManager:

    def __init__(self):

        self.registry = USBRegistryCollector()
        self.database = EvidenceDatabase()
        self.mounted = MountedDevicesCollector()

    def collect(self):

     devices = self.registry.collect()

     mounted = self.mounted.collect()

     for device in devices:
        self.database.insert_device(device)

     for item in mounted:
         self.database.insert_mounted_device(item)

     JSONReport.save(devices)

     return devices, mounted

    def close(self):

        self.database.close()