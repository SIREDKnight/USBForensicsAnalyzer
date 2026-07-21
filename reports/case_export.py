from importlib.resources import files
from pathlib import Path
import json
import zipfile

from utils.app_paths import AppPaths



class CaseReport:


    OUTPUT_FILE = AppPaths.OUTPUT_DIR / "case_report.json"



    @staticmethod
    def generate(
            case,
            devices,
            mounted,
            correlations,
            timeline):


        report = {}



        # ==========================================
        # CASE INFORMATION
        # ==========================================

        if case:

            report["case"] = {

                "id": case[0],
                "name": case[1],
                "created_at": case[2],
                "investigator": case[3]

            }

        else:

            report["case"] = None




        # ==========================================
        # USB DEVICES
        # ==========================================

        report["usb_devices"] = []


        for device in devices:


            report["usb_devices"].append(

                {

                    "manufacturer":
                    device.manufacturer,


                    "product":
                    device.product,


                    "revision":
                    device.revision,


                    "serial_number":
                    device.serial_number,


                    "registry_path":
                    device.registry_path

                }

            )




        # ==========================================
        # MOUNTED DEVICES
        # ==========================================

        report["mounted_devices"] = []


        for mount in mounted:


            report["mounted_devices"].append(

                {

                    "drive_letter":
                    mount.drive_letter,


                    "registry_name":
                    mount.registry_name,


                    "volume_guid":
                    mount.volume_guid

                }

            )




        # ==========================================
        # FORENSIC TIMELINE
        # ==========================================

        report["timeline"] = []


        for event in timeline:


            report["timeline"].append(

                {

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


                    "description":
                    event.get(
                        "description",
                        "UNKNOWN"
                    )

                }

            )




        # ==========================================
        # CORRELATION RESULTS
        # ==========================================

        report["correlations"] = []


        for correlation in correlations:


            report["correlations"].append(

                correlation

            )




        # ==========================================
        # SAVE JSON REPORT
        # ==========================================

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

    OUTPUT_DIR = AppPaths.EXPORTS_DIR

    @staticmethod
    def export(case_id):

        CaseExport.OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        zip_path = (
            CaseExport.OUTPUT_DIR /
            f"case_{case_id}_export.zip"
        )

        files = [

            AppPaths.OUTPUT_DIR / "case_report.pdf",

            AppPaths.OUTPUT_DIR / "case_report.json",

            AppPaths.OUTPUT_DIR / "usb_devices.json",

            AppPaths.DATABASE_DIR / "evidence.db"

        ]

        print("\n===== EXPORT DEBUG =====")

        for file in files:
            print(file)
            print("Exists:", file.exists())

        print("========================\n")

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