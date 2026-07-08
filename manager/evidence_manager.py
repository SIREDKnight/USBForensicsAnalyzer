from collector.registry import USBRegistryCollector
from collector.mounteddevices import MountedDevicesCollector
from collector.event_logs import EventLogCollector

from database.database import EvidenceDatabase

from reports.json_report import JSONReport
from reports.case_report import CaseReport
from reports.pdf_report import PDFReport

from utils.hash_utils import HashUtils

import getpass
from datetime import datetime



class EvidenceManager:


    def __init__(self):

        self.registry = USBRegistryCollector()

        self.mounted = MountedDevicesCollector()

        self.events = EventLogCollector()

        self.database = EvidenceDatabase()

        self.case_id = self.start_case()



    # ==================================================
    # CREATE NEW FORENSIC CASE
    # ==================================================

    def start_case(self):


        print("\n" + "=" * 70)

        print("CREATE NEW FORENSIC CASE")

        print("=" * 70)



        case_name = input(

            "Enter Case Name: "

        ).strip()



        if not case_name:


            case_name = (

                "USB Forensic Investigation"

            )



        investigator = getpass.getuser()



        timestamp = datetime.now().strftime(

            "%Y%m%d-%H%M%S"

        )



        generated_case_id = (

            f"CASE-{timestamp}"

        )



        database_id = self.database.create_case(

            generated_case_id,

            case_name,

            investigator

        )



        print("\n[+] Case Created")

        print(

            f"Case ID      : {generated_case_id}"

        )

        print(

            f"Case Name    : {case_name}"

        )

        print(

            f"Investigator : {investigator}"

        )

        print("=" * 70)



        return database_id



    # ==================================================
    # FULL ACQUISITION
    # ==================================================

    def collect(self):


        print("\n[+] Starting forensic acquisition...\n")



        devices = self.registry.collect()

        mounted = self.mounted.collect()

        events = self.events.collect()



        print(

            f"[+] USB Devices Found: {len(devices)}"

        )

        print(

            f"[+] Mounted Devices Found: {len(mounted)}"

        )

        print(

            f"[+] Event Logs Found: {len(events)}"

        )



        # ==============================================
        # SAVE USB DEVICES
        # ==============================================

        for device in devices:


            self.database.insert_device(

                device,

                self.case_id,

                HashUtils.sha256(

                    device.__dict__

                )

            )



        # ==============================================
        # SAVE MOUNTED DEVICES
        # ==============================================

        for mount in mounted:


            self.database.insert_mounted_device(

                mount,

                self.case_id,

                HashUtils.sha256(

                    mount.__dict__

                )

            )



        # ==============================================
        # SAVE EVENTS
        # ==============================================

        for event in events:


            self.database.insert_event_log(

                event["event_id"],

                event["source"],

                event["time"],

                event["description"],

                HashUtils.sha256(

                    event

                )

            )



        # ==============================================
        # TIMELINE
        # ==============================================

        timeline = self.build_timeline(

            events

        )


        for item in timeline:


            self.database.insert_timeline_event(

                item["time"],

                item["artifact"],

                item["description"],

                HashUtils.sha256(

                    item

                )

            )



        # ==============================================
        # CORRELATION
        # ==============================================

        correlations = self.correlate(

            devices,

            mounted

        )



        # ==============================================
        # REPORTS
        # ==============================================

        case = self.database.get_latest_case()



        JSONReport.save(

            devices

        )



        CaseReport.generate(

            case,

            devices,

            mounted,

            correlations,

            timeline

        )



        PDFReport.generate(

            case,

            devices,

            mounted,

            correlations,

            timeline

        )



        print("\n" + "=" * 70)

        print("ACQUISITION COMPLETE")

        print("=" * 70)

        print(

            f"Devices       : {len(devices)}"

        )

        print(

            f"Mounted       : {len(mounted)}"

        )

        print(

            f"Timeline      : {len(timeline)}"

        )

        print(

            f"Correlations  : {len(correlations)}"

        )

        print("=" * 70)



        return (

            devices,

            mounted,

            correlations,

            timeline

        )



    # ==================================================
    # TIMELINE BUILDER
    # ==================================================

    def build_timeline(self, events):


        timeline = []



        for event in events:


            timeline.append({

                "time":

                event["time"],


                "artifact":

                "EVENT_LOG",


                "description":

                event["description"]

            })



        timeline.sort(

            key=lambda x:x["time"]

        )



        return timeline



    # ==================================================
    # CORRELATION ENGINE
    # ==================================================

    def correlate(

            self,

            devices,

            mounted):


        correlations = []



        for device in devices:


            for mount in mounted:


                score = 40


                reasons = [


                    "USB device artifact detected",


                    "Mounted volume artifact detected"


                ]



                registry_text = (

                    mount.registry_name.lower()

                )



                if (

                    device.serial_number

                    and

                    device.serial_number.lower()

                    in registry_text

                ):


                    score += 40


                    reasons.append(

                        "Serial number match"

                    )



                if (

                    device.product

                    and

                    device.product.lower()

                    in registry_text

                ):


                    score += 20


                    reasons.append(

                        "Product name match"

                    )



                if score > 100:

                    score = 100



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



    # ==================================================
    # DEVICE QUERY
    # ==================================================

    def query_device(self, serial):


        device = self.database.get_device_by_serial(

            serial

        )


        timeline = self.database.get_timeline()



        return device, timeline



    # ==================================================
    # EXPORT
    # ==================================================

    def export_case(self):


        from reports.case_report import CaseExport


        CaseExport.export(

            self.case_id

        )



    # ==================================================
    # CLOSE
    # ==================================================

    def close(self):

        self.database.close()