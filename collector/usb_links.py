import winreg

from collector.base_collector import BaseCollector
from models.usb_link import USBLink


class USBLinksCollector(BaseCollector):
    """
    Collects Windows USB enumeration artifacts used for
    correlation between USBSTOR devices and mounted drives.

    Source:
    HKLM\\SYSTEM\\CurrentControlSet\\Enum\\USB
    """

    REGISTRY_PATH = r"SYSTEM\CurrentControlSet\Enum\USB"

    def collect(self):

        links = []

        try:

            root = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                self.REGISTRY_PATH
            )

            vendor_count = winreg.QueryInfoKey(root)[0]

            for vendor_index in range(vendor_count):

                try:

                    vendor_name = winreg.EnumKey(
                        root,
                        vendor_index
                    )

                    vendor_key = winreg.OpenKey(
                        root,
                        vendor_name
                    )

                    device_count = winreg.QueryInfoKey(
                        vendor_key
                    )[0]

                    for device_index in range(device_count):

                        try:

                            instance_name = winreg.EnumKey(
                                vendor_key,
                                device_index
                            )

                            instance_key = winreg.OpenKey(
                                vendor_key,
                                instance_name
                            )

                            container_id = self.read_value(
                                instance_key,
                                "ContainerID"
                            )

                            friendly_name = self.read_value(
                                instance_key,
                                "FriendlyName"
                            )

                            if friendly_name == "UNKNOWN":

                                friendly_name = self.read_value(
                                    instance_key,
                                    "DeviceDesc"
                                )

                            parent_prefix = self.read_value(
                                instance_key,
                                "ParentIdPrefix"
                            )

                            device_instance_id = (
                                f"{vendor_name}\\{instance_name}"
                            )

                            serial_number = instance_name

                            links.append(

                                USBLink(

                                    serial_number=serial_number,

                                    container_id=container_id,

                                    friendly_name=friendly_name,

                                    device_instance_id=device_instance_id,

                                    parent_id_prefix=parent_prefix

                                )

                            )

                            winreg.CloseKey(
                                instance_key
                            )

                        except Exception:

                            continue

                    winreg.CloseKey(
                        vendor_key
                    )

                except Exception:

                    continue

            winreg.CloseKey(
                root
            )

        except Exception as error:

            print(

                "[USB Links Collector Error]",

                error

            )

        return links

    # ==================================================
    # REGISTRY VALUE READER
    # ==================================================

    def read_value(

            self,

            key,

            value_name):

        try:

            value, _ = winreg.QueryValueEx(

                key,

                value_name

            )

            return str(value)

        except Exception:

            return "UNKNOWN"