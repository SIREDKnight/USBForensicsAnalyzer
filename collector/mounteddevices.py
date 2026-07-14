import winreg
import re

from collector.base_collector import BaseCollector
from models.mounted_device import MountedDevice
from utils.time_utils import TimeUtils


class MountedDevicesCollector(BaseCollector):
    """
    Collects mounted storage device mappings
    from Windows Registry.

    Source:
    SYSTEM\\MountedDevices
    """

    REGISTRY_PATH = r"SYSTEM\MountedDevices"



    def collect(self):

        devices = []

        key = None


        try:

            key = winreg.OpenKey(

                winreg.HKEY_LOCAL_MACHINE,

                self.REGISTRY_PATH

            )



            registry_timestamp = self.get_registry_timestamp(

                key

            )



            value_count = winreg.QueryInfoKey(

                key

            )[1]



            for i in range(value_count):

                try:


                    name, value, reg_type = winreg.EnumValue(

                        key,

                        i

                    )



                    # Only collect drive mappings

                    if not name.startswith(

                        "\\DosDevices\\"

                    ):

                        continue



                    drive_letter = name.replace(

                        "\\DosDevices\\",

                        ""

                    )



                    if not drive_letter:

                        continue



                    volume_guid = self.extract_volume_guid(

                        value

                    )


                    device_identifier = self.extract_device_identifier(

                        value

                    )


                    volume_serial = self.extract_volume_serial(

                        value

                    )



                    device = MountedDevice(


                        drive_letter=drive_letter,


                        registry_name=name,


                        volume_guid=volume_guid,


                        registry_timestamp=registry_timestamp,


                        device_identifier=device_identifier,


                        volume_serial=volume_serial

                    )



                    devices.append(device)



                except Exception:

                    continue



        except Exception as error:


            print(

                "[Mounted Devices Collector Error]",

                error

            )



        finally:


            try:

                if key:

                    winreg.CloseKey(

                        key

                    )


            except Exception:

                pass



        return devices



    # ==================================================
    # VOLUME GUID EXTRACTION
    # ==================================================

    def extract_volume_guid(

            self,

            value):


        try:


            if not isinstance(value, bytes):

                return "UNKNOWN"



            decoded = value.decode(

                "utf-16-le",

                errors="ignore"

            )



            match = re.search(

                r"Volume\{[0-9A-Fa-f\-]+\}",

                decoded,

                re.IGNORECASE

            )



            if match:

                return match.group(0)



            return self.extract_binary_guid(

                value

            )



        except Exception as error:


            print(

                "[Volume GUID Extraction Error]",

                error

            )



        return "UNKNOWN"



    # ==================================================
    # DEVICE IDENTIFIER EXTRACTION
    # ==================================================

    def extract_device_identifier(

            self,

            value):


        """
        Extracts device mapping information
        from MountedDevices binary data.
        """


        try:


            if not isinstance(value, bytes):

                return "UNKNOWN"



            decoded = value.decode(

                "utf-16-le",

                errors="ignore"

            )



            # Windows device path pattern

            if "\\\\?\\USB" in decoded.upper():


                return decoded.strip(

                    "\x00"

                )



            matches = re.findall(

                r"USBSTOR#[^\\x00]+",

                decoded,

                re.IGNORECASE

            )



            if matches:

                return matches[0]



        except Exception:

            pass



        return "UNKNOWN"



    # ==================================================
    # VOLUME SERIAL EXTRACTION
    # ==================================================

    def extract_volume_serial(

            self,

            value):


        try:


            if not isinstance(value, bytes):

                return "UNKNOWN"



            hex_data = value.hex()



            # Look for common 8 byte volume identifiers

            matches = re.findall(

                r"[0-9a-f]{8}",

                hex_data

            )



            if matches:

                return matches[0]



        except Exception:

            pass



        return "UNKNOWN"



    # ==================================================
    # BINARY GUID EXTRACTION
    # ==================================================

    def extract_binary_guid(

            self,

            value):


        try:


            hex_data = value.hex()



            matches = re.findall(

                r"[0-9a-f]{32}",

                hex_data

            )



            for raw in matches:


                guid = (

                    raw[6:8]

                    + raw[4:6]

                    + raw[2:4]

                    + raw[0:2]

                    + "-"

                    + raw[10:12]

                    + raw[8:10]

                    + "-"

                    + raw[14:16]

                    + raw[12:14]

                    + "-"

                    + raw[16:20]

                    + "-"

                    + raw[20:32]

                )


                return (

                    f"Volume{{{guid}}}"

                )



        except Exception:

            pass



        return "UNKNOWN"



    # ==================================================
    # REGISTRY TIMESTAMP
    # ==================================================

    def get_registry_timestamp(

            self,

            key):


        try:


            last_write = winreg.QueryInfoKey(

                key

            )[2]



            return TimeUtils.format_timestamp(

                last_write

            )



        except Exception:


            return "UNKNOWN"