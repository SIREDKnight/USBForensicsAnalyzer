from collector.registry import USBRegistryCollector
from collector.mounteddevices import MountedDevicesCollector
from collector.event_logs import EventLogCollector

from database.database import EvidenceDatabase

from reports.json_report import JSONReport
from reports.case_report import CaseReport
from reports.pdf_report import PDFReport

from utils.hash_utils import HashUtils



class EvidenceManager:


    def __init__(self):

        self.registry = USBRegistryCollector()

        self.mounted = MountedDevicesCollector()

        self.events = EventLogCollector()

        self.database = EvidenceDatabase()

        self.case_id = self.start_case()



    # ==================================================
    # CASE MANAGEMENT
    # ==================================================

    def start_case(self):

        case = self.database.get_latest_case()


        if case:

            return case[0]



        return self.database.create_case(

            "USB Investigation Case 001",

            "Analyst"

        )



    # ==================================================
    # FULL ACQUISITION
    # ==================================================

    def collect(self):


        print("\n[+] Starting forensic acquisition...\n")



        # Collect artifacts

        devices = self.registry.collect()

        mounted = self.mounted.collect()

        events = self.events.collect()



        print("\n===== DEBUG =====")

        print("Events collected:")

        print(events)



        # ==============================================
        # SAVE USB DEVICES
        # ==============================================


        for device in devices:


            record_hash = HashUtils.sha256(

                device.to_dict()

            )


            self.database.insert_device(

                device,

                self.case_id,

                record_hash

            )



        # ==============================================
        # SAVE MOUNTED DEVICES
        # ==============================================


        for mount in mounted:


            record_hash = HashUtils.sha256(

                mount.to_dict()

            )


            self.database.insert_mounted_device(

                mount,

                self.case_id,

                record_hash

            )



        # ==============================================
        # SAVE EVENT LOGS
        # ==============================================


        for event in events:


            record_hash = HashUtils.sha256(

                event

            )


            self.database.insert_event_log(

                event,

                record_hash

            )



        # ==============================================
        # BUILD TIMELINE
        # ==============================================


        timeline = self.build_timeline(

            events

        )



        print("\nTimeline built:")

        print(timeline)

        print("=================\n")



        for item in timeline:


            self.database.insert_timeline_event(

                item["time"],

                item["artifact"],

                item["description"]

            )



        # ==============================================
        # CORRELATION
        # ==============================================


        correlations = self.correlate(

            devices,

            mounted

        )



        # ==============================================
        # REPORT GENERATION
        # ==============================================


        JSONReport.save(

            devices

        )


        case = self.database.get_latest_case()



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


            timeline.append(

                {

                    "time":
                    event["time"],


                    "artifact":
                    "EVENT_LOG",


                    "description":
                    event["description"]

                }

            )



        timeline.sort(

            key=lambda x: x["time"]

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


                score = 0

                reasons = []


                # Base evidence:
                # USB artifact exists
                score += 20

                reasons.append(
                    "USB device artifact detected"
                )


                # Mounted evidence exists
                score += 20

                reasons.append(
                    "Mounted volume artifact detected"
                )



                device_text = (

                    str(device.manufacturer) +

                    str(device.product)

                ).lower()



                mount_text = (

                    str(mount.registry_name)

                ).lower()



                # Serial number correlation

                if (

                    device.serial_number

                    and

                    device.serial_number.lower()
                    in mount_text

                ):


                    score += 50


                    reasons.append(

                        "Serial number match found"

                    )



                # Product correlation

                if (

                    device.product

                    and

                    device.product.lower()
                    in mount_text

                ):


                    score += 10


                    reasons.append(

                        "Product name match found"

                    )



                # Manufacturer correlation

                if (

                    device.manufacturer

                    and

                    device.manufacturer.lower()
                    in mount_text

                ):


                    score += 10


                    reasons.append(

                        "Manufacturer match found"

                    )



                # Maximum confidence = 100

                if score > 100:

                    score = 100



                # Only report meaningful correlations

                if score >= 40:


                    correlations.append(

                        {

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

                        }

                    )


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
    # EXPORT CASE
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