from pathlib import Path
import json
import zipfile

from utils.hash_utils import HashUtils



class CaseReport:


    OUTPUT_FILE = Path("output") / "case_report.json"



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


                "name":
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


            report["usb_devices"].append({

                "manufacturer":

                device.manufacturer,


                "product":

                device.product,


                "revision":

                device.revision,


                "serial_number":

                device.serial_number,


                "registry_path":

                device.registry_path,


                "registry_time":

                device.registry_time,


                "sha256":

                HashUtils.sha256(

                    device.__dict__

                )

            })



        # ==================================================
        # MOUNTED DEVICES
        # ==================================================

        report["mounted_devices"] = []



        for mount in mounted:


            report["mounted_devices"].append({

                "drive_letter":

                mount.drive_letter,


                "registry_name":

                mount.registry_name,


                "volume_guid":

                mount.volume_guid,


                "registry_time":

                mount.registry_time,


                "sha256":

                HashUtils.sha256(

                    mount.__dict__

                )

            })



        # ==================================================
        # TIMELINE
        # ==================================================

        report["timeline"] = []



        for event in timeline:


            report["timeline"].append({

                "time":

                event["time"],


                "artifact":

                event["artifact"],


                "description":

                event["description"],


                "sha256":

                HashUtils.sha256(

                    event

                )

            })



        # ==================================================
        # CORRELATION RESULTS
        # ==================================================

        report["correlations"] = correlations



        # ==================================================
        # SUMMARY
        # ==================================================

        report["summary"] = {


            "usb_devices":

            len(devices),


            "mounted_devices":

            len(mounted),


            "timeline_events":

            len(timeline),


            "correlations":

            len(correlations)

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



    OUTPUT_DIR = Path("output")



    @staticmethod
    def export(case_id):


        CaseExport.OUTPUT_DIR.mkdir(

            exist_ok=True

        )



        zip_path = (

            CaseExport.OUTPUT_DIR /

            f"case_{case_id}_export.zip"

        )



        files = [


            CaseExport.OUTPUT_DIR /

            "case_report.pdf",


            CaseExport.OUTPUT_DIR /

            "case_report.json",


            CaseExport.OUTPUT_DIR /

            "usb_devices.json",


            Path("database") /

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