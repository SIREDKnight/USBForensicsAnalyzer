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

        self.case_id = None



    # ==================================================
    # CASE CREATION
    # ==================================================

    def create_case(

            self,

            case_id,

            case_name,

            investigator):


        self.case_id = self.database.create_case(

            case_id,

            case_name,

            investigator

        )


        return self.case_id



    # ==================================================
    # FULL ACQUISITION
    # ==================================================

    def collect(self):


        if self.case_id is None:

            raise Exception(

                "No active case. Create a case first."

            )



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


            record_hash = HashUtils.sha256(

                device.__dict__

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

                mount.__dict__

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

                event.get(

                    "event_id",

                    0

                ),

                event.get(

                    "source",

                    "Windows Event Log"

                ),

                event.get(

                    "time",

                    "UNKNOWN"

                ),

                event.get(

                    "description",

                    "UNKNOWN"

                ),

                record_hash

            )



        # ==============================================
        # BUILD TIMELINE
        # ==============================================

        timeline = self.build_timeline(

            events

        )



        for item in timeline:


            record_hash = HashUtils.sha256(

                item

            )


            self.database.insert_timeline_event(

                item["time"],

                item["artifact"],

                item["description"],

                record_hash

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


            timeline.append({

                "time":

                event.get(

                    "time",

                    "UNKNOWN"

                ),


                "artifact":

                "EVENT_LOG",


                "description":

                event.get(

                    "description",

                    "UNKNOWN"

                )

            })



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


                score = 40


                reasons = [

                    "USB device artifact detected",

                    "Mounted volume artifact detected"

                ]



                registry_name = (

                    mount.registry_name.lower()

                    if mount.registry_name

                    else ""

                )



                if (

                    device.serial_number

                    and

                    device.serial_number.lower()

                    in registry_name

                ):


                    score += 40


                    reasons.append(

                        "Serial number match"

                    )



                if (

                    device.product

                    and

                    device.product.lower()

                    in registry_name

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

                    reasons,


                    "evidence":

                    {

                        "usb_registry_path":

                        device.registry_path,


                        "mounted_registry_name":

                        mount.registry_name,


                        "volume_guid":

                        mount.volume_guid

                    }

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