import winreg
from datetime import datetime

import win32api

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


                            registry_time = self.get_registry_time(

                                serial_key

                            )



                            device = USBDevice(

                                manufacturer=manufacturer,

                                product=device_entry,

                                revision="Unknown",

                                serial_number=device_entry,

                                registry_path=serial_path,

                                registry_time=registry_time

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





    # ==================================================
    # REGISTRY TIMESTAMP
    # ==================================================

    def get_registry_time(self, key):

        try:

            info = win32api.RegQueryInfoKey(

                key

            )


            filetime = info[2]


            # Convert Windows FILETIME to Unix timestamp

            timestamp = (

                filetime - 116444736000000000

            ) / 10000000


            return datetime.fromtimestamp(

                timestamp

            ).strftime(

                "%Y-%m-%d %H:%M:%S"

            )


        except Exception as e:

            print(

                "[Registry timestamp error]",

                repr(e)

            )

            return "UNKNOWN"




    # ==================================================
    # SUBKEY ENUMERATION
    # ==================================================

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