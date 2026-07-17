from collector.registry import USBRegistryCollector
from collector.mounteddevices import MountedDevicesCollector
from collector.event_logs import EventLogCollector
from collector.usb_links import USBLinksCollector
from collector.live_usb import LiveUSBCollector


from database.database import EvidenceDatabase

from reports.json_report import JSONReport
from reports.case_report import CaseReport
from reports.pdf_report import PDFReport

from timeline.timeline_builder import TimelineBuilder

from utils.hash_utils import HashUtils



class EvidenceManager:


    def __init__(self):

        self.registry = USBRegistryCollector()

        self.mounted = MountedDevicesCollector()

        self.events = EventLogCollector()

        self.usb_links = USBLinksCollector()

        self.live_usb = LiveUSBCollector()

        self.timeline_builder = TimelineBuilder()

        self.database = EvidenceDatabase()

        self.case_id = None



    # ==================================================
    # CASE CREATION
    # ==================================================

    def create_case(
            self,
            case_name,
            investigator,
            generated_case_id):


        self.case_id = self.database.create_case(

            generated_case_id,

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


        print(
            "\n[+] Starting forensic acquisition...\n"
        )


        devices = self.registry.collect()

        mounted = self.mounted.collect()

        events = self.events.collect()

        usb_links = self.usb_links.collect()

        live_usb = self.live_usb.collect()



        print(
            f"[+] USB Devices Found: {len(devices)}"
        )

        print(
            f"[+] Mounted Devices Found: {len(mounted)}"
        )

        print(
            f"[+] Event Logs Found: {len(events)}"
        )

        print(
            f"[+] USB Link Artifacts Found: {len(usb_links)}"
        )

        print(
            f"[+] Live USB Devices Found: {len(live_usb)}"
        )



        # ==================================================
        # STORE DEVICES
        # ==================================================

        for device in devices:

            self.database.insert_device(

                device,

                self.case_id,

                HashUtils.sha256(
                    device.to_dict()
                )

            )



        # ==================================================
        # STORE MOUNTED DEVICES
        # ==================================================

        for mount in mounted:

            self.database.insert_mounted_device(

                mount,

                self.case_id,

                HashUtils.sha256(
                    mount.to_dict()
                )

            )



        # ==================================================
        # STORE EVENTS
        # ==================================================

        for event in events:

            self.database.insert_event_log(

                event["event_id"],

                event["source"],

                event["time"],

                event["description"],

                HashUtils.sha256(event),

                self.case_id

            )



        # ==================================================
        # BUILD TIMELINE
        # ==================================================

        timeline = self.timeline_builder.build(

            devices,

            mounted,

            events

        )



        for item in timeline:

            self.database.insert_timeline_event(

                item.time,

                item.artifact,

                item.description,

                HashUtils.sha256(
                    item.to_dict()
                ),

                item.event_id,

                item.source,

                self.case_id

            )



        # ==================================================
        # CORRELATION
        # ==================================================

        correlations = self.correlate(

            devices,

            mounted,

            usb_links,

            live_usb

        )



        # ==================================================
        # REPORT GENERATION
        # ==================================================

        JSONReport.save(

            devices

        )


        case = self.database.get_latest_case()



        timeline_dict = [

            event.to_dict()

            for event in timeline

        ]



        CaseReport.generate(

            case,

            devices,

            mounted,

            correlations,

            timeline_dict

        )


        PDFReport.generate(

            case,

            devices,

            mounted,

            correlations,

            timeline_dict

        )



        return (

            devices,

            mounted,

            correlations,

            timeline_dict

        )



    # ==================================================
    # CORRELATION ENGINE
    # ==================================================

    def correlate(

            self,

            devices,

            mounted,

            usb_links,

            live_usb):


        results = []



        for device in devices:


            matched_live = None

            matched_mount = None


            score = 20


            reasons = [

                "USB registry artifact found"

            ]



            # =========================================
            # MATCH USBSTOR WITH LIVE USB
            # =========================================

            for live in live_usb:


                device_instance = (

                    device.registry_path

                    .split("USBSTOR\\")

                    [-1]

                    .lower()

                    .replace("\\", "")

                )



                live_instance = (

                    live["instance_id"]

                    .split("USBSTOR\\")

                    [-1]

                    .lower()

                    .replace("\\", "")

                )



                if (

                    device_instance

                    in

                    live_instance

                ):


                    matched_live = live

                    score += 40


                    reasons.append(

                        "USBSTOR device matched active USB device"

                    )


                    break



            # =========================================
            # MATCH DRIVE LETTER
            # =========================================

            if matched_live:


                for mount in mounted:


                    if (

                        mount.drive_letter

                        in

                        matched_live["drive_letters"]

                    ):


                        matched_mount = mount


                        score += 40


                        reasons.append(

                            "Active USB drive mapped to volume"

                        )


                        break



            results.append({


                "manufacturer":

                    device.manufacturer,


                "product":

                    device.product,


                "serial_number":

                    device.serial_number,


                "drive_letter":

                    (

                        matched_mount.drive_letter

                        if matched_mount

                        else None

                    ),


                "volume_guid":

                    (

                        matched_mount.volume_guid

                        if matched_mount

                        else None

                    ),


                "container_id":

                    device.container_id,


                "friendly_name":

                    device.friendly_name,


                "confidence":

                    min(score,100),


                "reasons":

                    reasons


            })


        return results



    # ==================================================
    # QUERY
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