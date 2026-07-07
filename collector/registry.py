import winreg

from collector.base_collector import BaseCollector
from models.device import USBDevice


class USBRegistryCollector(BaseCollector):

    REGISTRY_PATH = r"SYSTEM\CurrentControlSet\Enum\USBSTOR"


    def collect(self):

        devices = []


        try:

            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                self.REGISTRY_PATH
            )


            manufacturer_keys = self.get_subkeys(key)


            for manufacturer in manufacturer_keys:


                manufacturer_path = (
                    self.REGISTRY_PATH +
                    "\\" +
                    manufacturer
                )


                try:

                    device_key = winreg.OpenKey(
                        winreg.HKEY_LOCAL_MACHINE,
                        manufacturer_path
                    )


                    device_entries = self.get_subkeys(device_key)


                    for device_entry in device_entries:


                        serial_path = (
                            manufacturer_path +
                            "\\" +
                            device_entry
                        )


                        try:

                            serial_key = winreg.OpenKey(
                                winreg.HKEY_LOCAL_MACHINE,
                                serial_path
                            )


                            device = USBDevice(

                                manufacturer=manufacturer,

                                product=device_entry,

                                revision="Unknown",

                                serial_number=device_entry,

                                registry_path=serial_path

                            )


                            devices.append(device)


                        except Exception:

                            continue


                except Exception:

                    continue


        except Exception as e:

            print(
                "[USB Registry Error]",
                e
            )


        return devices



    def get_subkeys(self, key):

        result = []


        index = 0


        while True:

            try:

                name = winreg.EnumKey(
                    key,
                    index
                )

                result.append(name)

                index += 1


            except OSError:

                break


        return result