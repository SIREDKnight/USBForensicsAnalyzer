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


                name, value, reg_type = winreg.EnumValue(
                    key,
                    i
                )


                drive_letter = None


                volume_guid = None



                if name.startswith(
                    "\\DosDevices\\"
                ):


                    drive_letter = name.replace(
                        "\\DosDevices\\",
                        ""
                    )



                elif name.startswith(
                    r"\??\Volume"
                ):


                    volume_guid = name



                if drive_letter:


                    devices.append(

                        MountedDevice(

                            drive_letter=drive_letter,

                            registry_name=name,

                            volume_guid=volume_guid

                        )

                    )


        except Exception as e:


            print(
                "[Mounted Devices Error]",
                e
            )


        return devices