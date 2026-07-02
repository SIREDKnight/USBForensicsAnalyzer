import json
from pathlib import Path

OUTPUT_FILE = Path("output") / "usb_devices.json"


class JSONReport:

    @staticmethod
    def save(devices):

        data = []

        for device in devices:

            data.append(
                {
                    "manufacturer": device.manufacturer,
                    "product": device.product,
                    "revision": device.revision,
                    "serial_number": device.serial_number,
                    "registry_path": device.registry_path
                }
            )

        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

            json.dump(data, file, indent=4)

        print(f"\nEvidence saved to {OUTPUT_FILE}")