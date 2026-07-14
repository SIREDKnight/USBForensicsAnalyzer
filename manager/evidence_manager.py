from collector.registry import USBRegistryCollector
from collector.mounteddevices import MountedDevicesCollector
from collector.event_logs import EventLogCollector
from collector.usb_links import USBLinksCollector

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

                HashUtils.sha256(

                    event

                ),

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

            usb_links

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
    # IMPROVED CORRELATION ENGINE
    # ==================================================

        # ==================================================
    # CORRELATION ENGINE
    # ==================================================

        # ==================================================
    # CORRELATION ENGINE
    # ==================================================

    def correlate(
        self,
        devices,
        mounted,
        usb_links):


        results = []


        for device in devices:

            matched = False

            # ---------------------------------
            # CHECK EVERY MOUNT FOR THIS DEVICE
            # ---------------------------------

            for mount in mounted:

                score = 40

                reasons = [
                    "USB device enumeration registry evidence found"
                ]

                device_match = False

                identifier = str(
                    getattr(
                        mount,
                        "device_identifier",
                        "UNKNOWN"
                    )
                ).lower()

                identifier = identifier.replace("#", "&")

                vendor = device.manufacturer.lower()
                product = device.product.lower()
                revision = device.revision.lower()

                checks = 0

                if vendor in identifier:
                    checks += 1

                if product in identifier:
                    checks += 1

                if revision.replace(".", "") in identifier.replace(".", ""):
                    checks += 1

                if checks >= 2:
                    device_match = True

                serial_clean = device.serial_number.lower().split("&")[0]

                if serial_clean in identifier:
                    device_match = True

                if device.registry_path.lower() in identifier:
                    device_match = True

                if device_match:

                    matched = True

                    score += 40

                    reasons.append(
                        "Mounted volume matched USB storage identifier"
                    )

                    if getattr(device, "container_id", "UNKNOWN") != "UNKNOWN":

                        score += 10

                        reasons.append(
                            "Device ContainerID recovered from registry"
                        )

                    if getattr(device, "friendly_name", "UNKNOWN") != "UNKNOWN":

                        score += 10

                        reasons.append(
                            "Friendly device name recovered"
                        )

                    results.append({

                        "manufacturer":
                            device.manufacturer,

                        "product":
                            device.product,

                        "serial_number":
                            device.serial_number,

                        "drive_letter":
                            mount.drive_letter,

                        "volume_guid":
                            mount.volume_guid,

                        "container_id":
                            getattr(
                                device,
                                "container_id",
                                "UNKNOWN"
                            ),

                        "friendly_name":
                            getattr(
                                device,
                                "friendly_name",
                                "UNKNOWN"
                            ),

                        "confidence":
                            score,

                        "reasons":
                            reasons

                    })

                    break

            # ---------------------------------
            # DEVICE EXISTS BUT NO MOUNT FOUND
            # ---------------------------------

            if not matched:

                results.append({

                    "manufacturer":
                        device.manufacturer,

                    "product":
                        device.product,

                    "serial_number":
                        device.serial_number,

                    "drive_letter":
                        None,

                    "volume_guid":
                        None,

                    "container_id":
                        getattr(
                            device,
                            "container_id",
                            "UNKNOWN"
                        ),

                    "friendly_name":
                        getattr(
                            device,
                            "friendly_name",
                            "UNKNOWN"
                        ),

                    "confidence":
                        50,

                    "reasons": [

                        "USB device enumeration registry evidence found",

                        "Device metadata recovered",

                        "No mounted volume mapping found"

                    ]

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