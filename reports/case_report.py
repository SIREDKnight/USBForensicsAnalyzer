from pathlib import Path
import json
import zipfile
import os

from utils.hash_utils import HashUtils
from utils.app_paths import AppPaths


AppPaths.initialize()



class CaseReport:


    OUTPUT_DIR = (

        Path(os.getenv("LOCALAPPDATA"))

        / "USBForensicsAnalyzer"

        / "output"

    )


    OUTPUT_FILE = OUTPUT_DIR / "case_report.json"



    @staticmethod
    def generate(

            case,

            devices,

            mounted,

            correlations,

            timeline):


        report = {}



        # ==================================================
        # CASE INFORMATION
        # ==================================================

        if case:


            report["case"] = {


                "id":

                case["id"],


                "case_name":

                case["case_name"],


                "created_at":

                case["created_at"],


                "investigator":

                case["investigator"]

            }


        else:


            report["case"] = None



        # ==================================================
        # USB DEVICES
        # ==================================================

        report["usb_devices"] = []



        for device in devices:


            record = device.to_dict()



            record["sha256"] = HashUtils.sha256(

                record

            )



            report["usb_devices"].append(

                record

            )



        # ==================================================
        # MOUNTED DEVICES
        # ==================================================

        report["mounted_devices"] = []



        for mount in mounted:


            record = mount.to_dict()



            record["sha256"] = HashUtils.sha256(

                record

            )



            report["mounted_devices"].append(

                record

            )



        # ==================================================
        # TIMELINE
        # ==================================================

        report["timeline"] = []



        for event in timeline:


            if hasattr(event, "to_dict"):


                event = event.to_dict()



            record = {


                "time":

                event.get(

                    "time",

                    "UNKNOWN"

                ),


                "artifact":

                event.get(

                    "artifact",

                    "UNKNOWN"

                ),


                "event_id":

                event.get(

                    "event_id",

                    None

                ),


                "source":

                event.get(

                    "source",

                    None

                ),


                "description":

                event.get(

                    "description",

                    "UNKNOWN"

                )

            }



            record["sha256"] = HashUtils.sha256(

                record

            )



            report["timeline"].append(

                record

            )



        # ==================================================
        # USB DEVICE TO DRIVE CORRELATIONS
        # ==================================================

        report["correlations"] = []



        for correlation in correlations:


            record = {


                # ------------------------------------------
                # USB DEVICE INFORMATION
                # ------------------------------------------

                "manufacturer":

                correlation.get(

                    "manufacturer",

                    "UNKNOWN"

                ),


                "product":

                correlation.get(

                    "product",

                    "UNKNOWN"

                ),


                "serial_number":

                correlation.get(

                    "serial_number",

                    "UNKNOWN"

                ),



                # ------------------------------------------
                # DRIVE INFORMATION
                # ------------------------------------------

                "drive_letter":

                correlation.get(

                    "drive_letter",

                    "UNKNOWN"

                ),


                "volume_guid":

                correlation.get(

                    "volume_guid",

                    "UNKNOWN"

                ),



                # ------------------------------------------
                # USB LINK ARTIFACTS
                # ------------------------------------------

                "container_id":

                correlation.get(

                    "container_id",

                    "UNKNOWN"

                ),


                "friendly_name":

                correlation.get(

                    "friendly_name",

                    "UNKNOWN"

                ),



                # ------------------------------------------
                # CORRELATION ANALYSIS
                # ------------------------------------------

                "confidence":

                correlation.get(

                    "confidence",

                    0

                ),


                "reasons":

                correlation.get(

                    "reasons",

                    []

                )

            }



            record["sha256"] = HashUtils.sha256(

                record

            )



            report["correlations"].append(

                record

            )



        # ==================================================
        # SUMMARY
        # ==================================================

        report["summary"] = {


            "usb_devices":

            len(devices),



            "mounted_devices":

            len(mounted),



            "timeline_events":

            len(report["timeline"]),



            "correlations":

            len(report["correlations"])

        }



        # ==================================================
        # SAVE REPORT
        # ==================================================

        CaseReport.OUTPUT_FILE.parent.mkdir(

            exist_ok=True

        )



        with open(

            CaseReport.OUTPUT_FILE,

            "w",

            encoding="utf-8"

        ) as file:


            json.dump(

                report,

                file,

                indent=4

            )



        print(

            f"\n[+] Case report generated: {CaseReport.OUTPUT_FILE}"

        )







# ==================================================
# CASE EXPORT
# ==================================================

class CaseExport:



    OUTPUT_DIR = (

        Path(os.getenv("LOCALAPPDATA"))

        / "USBForensicsAnalyzer"

        / "output"

    )



    @staticmethod
    def export(case_id):


        CaseExport.OUTPUT_DIR.mkdir(

            exist_ok=True

        )



        zip_path = (

            CaseExport.OUTPUT_DIR

            /

            f"case_{case_id}_export.zip"

        )



        files = [


            CaseExport.OUTPUT_DIR

            /

            "case_report.pdf",



            CaseExport.OUTPUT_DIR

            /

            "case_report.json",



            CaseReport.OUTPUT_DIR

            /

            "usb_devices.json",



            Path(os.getenv("LOCALAPPDATA"))

            /

            "USBForensicsAnalyzer"

            /

            "database"

            /

            "evidence.db"


        ]



        with zipfile.ZipFile(

            zip_path,

            "w",

            zipfile.ZIP_DEFLATED

        ) as archive:


            for file in files:


                if file.exists():


                    archive.write(

                        file,

                        arcname=file.name

                    )



        print(

            f"\n[+] Case exported: {zip_path}"

        )