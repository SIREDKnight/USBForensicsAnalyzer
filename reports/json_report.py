import json
from pathlib import Path
import os

from utils.app_paths import AppPaths
from utils.hash_utils import HashUtils



# Initialize application folders

AppPaths.initialize()



class JSONReport:


    OUTPUT_DIR = AppPaths.OUTPUT_DIR

    OUTPUT_FILE = OUTPUT_DIR / "usb_devices.json"



    @staticmethod
    def save(devices):


        JSONReport.OUTPUT_FILE.parent.mkdir(

            exist_ok=True

        )



        data = []



        for device in devices:


            record = device.to_dict()



            record["sha256"] = HashUtils.sha256(

                record

            )



            data.append(

                record

            )



        with open(

            JSONReport.OUTPUT_FILE,

            "w",

            encoding="utf-8"

        ) as file:


            json.dump(

                data,

                file,

                indent=4

            )



        print(

            f"\n[+] Evidence saved to {JSONReport.OUTPUT_FILE}"

        )