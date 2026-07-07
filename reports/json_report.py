import json

from pathlib import Path



class JSONReport:


    OUTPUT_FILE = Path("output") / "usb_devices.json"



    @staticmethod
    def save(devices):


        JSONReport.OUTPUT_FILE.parent.mkdir(

            exist_ok=True

        )


        data = []



        for device in devices:


            data.append(

                device.to_dict()

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

            f"\nEvidence saved to {JSONReport.OUTPUT_FILE}"

        )