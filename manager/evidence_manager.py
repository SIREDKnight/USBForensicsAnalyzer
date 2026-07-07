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



    def start_case(self):

        case = self.database.get_latest_case()

        if case:

            return case[0]


        return self.database.create_case(
            "USB Investigation Case 001",
            "Analyst"
        )



    def collect(self):


        devices = self.registry.collect()


        mounted = self.mounted.collect()


        events = self.events.collect()



        print("\n===== DEBUG =====")

        print("Events collected:")

        print(events)



        # Save USB devices

        for device in devices:

            self.database.insert_device(
                device,
                self.case_id
            )



        # Save mounted devices

        for mount in mounted:

            self.database.insert_mounted_device(
                mount,
                self.case_id
            )



        # Save events

        for event in events:

            self.database.insert_event_log(
                event["event_id"],
                event["source"],
                event["time"],
                event["description"]
            )



        # Correlation

        correlations = self.correlate(
            devices,
            mounted
        )



        # Timeline

        timeline = self.build_timeline(
            events
        )



        print("\nTimeline built:")

        print(timeline)

        print("=================\n")



        JSONReport.save(
            devices
        )


        CaseReport.generate(
            self.database.get_latest_case(),
            devices,
            mounted,
            correlations,
            timeline
        )



        return (
            devices,
            mounted,
            correlations,
            timeline
        )



    def build_timeline(self, events):

        timeline = []


        for event in events:

            timeline.append({

                "time": event["time"],

                "artifact": "EVENT_LOG",

                "description": event["description"]

            })


        timeline.sort(
            key=lambda x:x["time"]
        )


        return timeline




    # ==================================
    # UPDATED CORRELATION ENGINE
    # ==================================

    def correlate(self, devices, mounted):

        correlations = []


        for device in devices:

            for mount in mounted:


                score = 0

                reasons = []


                device_text = (
                    str(device.manufacturer) +
                    str(device.product) +
                    str(device.serial_number)
                ).lower()



                mount_text = (
                    str(mount.drive_letter) +
                    str(mount.registry_name)
                ).lower()



                # Serial match

                if (
                    device.serial_number
                    and
                    str(device.serial_number).lower()
                    in mount_text
                ):

                    score += 70

                    reasons.append(
                        "Serial number found in mounted artifact"
                    )



                # Product match

                if (
                    device.product
                    and
                    str(device.product).lower()
                    in mount_text
                ):

                    score += 20

                    reasons.append(
                        "Product name match"
                    )



                # Existing USB + Mounted evidence

                if score == 0:

                    score += 30

                    reasons.append(
                        "USB device and mounted volume "
                        "exist during acquisition"
                    )



                if score >= 30:

                    correlations.append({

                        "manufacturer":
                            device.manufacturer,

                        "product":
                            device.product,

                        "serial_number":
                            device.serial_number,

                        "drive_letter":
                            mount.drive_letter,

                        "confidence":
                            score,

                        "reasons":
                            reasons

                    })


        return correlations



    def close(self):

        self.database.close()