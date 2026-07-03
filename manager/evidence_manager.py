from collector.registry import USBRegistryCollector
from database.database import EvidenceDatabase
from reports.json_report import JSONReport


class EvidenceManager:

    def __init__(self):

        self.registry = USBRegistryCollector()
        self.database = EvidenceDatabase()

    def collect(self):

        devices = self.registry.collect()

        for device in devices:
            self.database.insert_device(device)

        JSONReport.save(devices)

        return devices

    def close(self):

        self.database.close()