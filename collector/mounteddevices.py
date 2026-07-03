import winreg

from collector.base_collector import BaseCollector
from models.mounted_device import MountedDevice


class MountedDevicesCollector(BaseCollector):

    REGISTRY_PATH = r"SYSTEM\MountedDevices"

    def collect(self):

        devices = []

        try:

            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                self.REGISTRY_PATH
            )

            value_count = winreg.QueryInfoKey(key)[1]

            for i in range(value_count):

                name, value, reg_type = winreg.EnumValue(key, i)

                if name.startswith("\\DosDevices\\"):

                    drive_letter = name.replace("\\DosDevices\\", "")

                    devices.append(
                        MountedDevice(
                            drive_letter,
                            name
                        )
                    )

        except Exception as e:

            print(e)

        return devices