import re
import winreg

from models.device import USBDevice
from collector.base_collector import BaseCollector


class USBRegistryCollector(BaseCollector):

    REGISTRY_PATH = r"SYSTEM\CurrentControlSet\Enum\USBSTOR"

    def collect(self):

        devices = []

        try:

            root = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                self.REGISTRY_PATH
            )

            model_count = winreg.QueryInfoKey(root)[0]

            for i in range(model_count):

                model_name = winreg.EnumKey(root, i)

                model_key = winreg.OpenKey(root, model_name)

                serial_count = winreg.QueryInfoKey(model_key)[0]

                manufacturer = self.extract_vendor(model_name)
                product = self.extract_product(model_name)
                revision = self.extract_revision(model_name)

                for j in range(serial_count):

                    serial = winreg.EnumKey(model_key, j)

                    registry_path = (
                        self.REGISTRY_PATH
                        + "\\"
                        + model_name
                        + "\\"
                        + serial
                    )

                    devices.append(
                        USBDevice(
                            manufacturer,
                            product,
                            revision,
                            serial,
                            registry_path
                        )
                    )

        except FileNotFoundError:

            print("USBSTOR Registry key not found.")

        return devices

    def extract_vendor(self, text):

        match = re.search(r"Ven_([^&]+)", text)

        return match.group(1) if match else "Unknown"

    def extract_product(self, text):

        match = re.search(r"Prod_([^&]+)", text)

        if match:

            return match.group(1).replace("_", " ")

        return "Unknown"

    def extract_revision(self, text):

        match = re.search(r"Rev_([^&]+)", text)

        return match.group(1) if match else "Unknown"