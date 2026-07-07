from asyncio import events

from collector.registry import USBRegistryCollector
from collector.mounteddevices import MountedDevicesCollector
from collector.event_logs import EventLogCollector

from database.database import EvidenceDatabase
from reports.json_report import JSONReport
from reports.case_report import CaseReport


class EvidenceManager:

    def __init__(self):

        self.registry = USBRegistryCollector()
        self.mounted = MountedDevicesCollector()
        self.events = EventLogCollector()

        self.database = EvidenceDatabase()

        self.case_id = self.start_case()

    # -------------------------
    # CASE
    # -------------------------
    def start_case(self):

        case = self.database.get_latest_case()

        if case:
            return case[0]

        return self.database.create_case(
            "USB Investigation Case",
            "Analyst"
        )

    # -------------------------
    # MAIN PIPELINE
    # -------------------------
    def collect(self):

        devices = self.registry.collect()
        mounted = self.mounted.collect()
        events = self.events.collect()

        correlations = self.correlate(devices, mounted)

        timeline = self.build_timeline(events)

        print("\n===== DEBUG =====")
        print("Events collected:")
        print(events)

        print("\nTimeline built:")
        print(timeline)
        print("=================\n")

        # DATABASE STORAGE
        for d in devices:
            self.database.insert_device(d, self.case_id)

        for m in mounted:
            self.database.insert_mounted_device(m, self.case_id)

        for e in events:
            self.database.insert_event_log(
                e["event_id"],
                e["source"],
                e["time"],
                e["description"]
            )

        # REPORTS
        JSONReport.save(devices)

        CaseReport.generate(
            self.database.get_latest_case(),
            devices,
            mounted,
            correlations,
            timeline
        )

        return devices, mounted, correlations, timeline

    # -------------------------
    # TIMELINE (REAL ONLY)
    # -------------------------
    def build_timeline(self, events):

        timeline = []

        for e in events:

            timeline.append({
                "time": e["time"],
                "artifact": "EVENT_LOG",
                "description": e["description"]
            })

        timeline.sort(key=lambda x: x["time"])

        return timeline

    # -------------------------
    # CORRELATION (NO TIME)
    # -------------------------
    def correlate(self, devices, mounted):

        results = []

        for d in devices:
            for m in mounted:

                score = 0
                reasons = []

                if d.serial_number in m.registry_name:
                    score += 60
                    reasons.append("Serial match")

                if d.product.lower() in m.registry_name.lower():
                    score += 20
                    reasons.append("Product match")

                if score >= 60:

                    results.append({
                        "device": d,
                        "drive_letter": m.drive_letter,
                        "score": score,
                        "reasons": reasons
                    })

        return results

    # -------------------------
    # CLOSE
    # -------------------------
    def close(self):
        self.database.close()