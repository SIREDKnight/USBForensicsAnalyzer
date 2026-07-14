from importlib.metadata import metadata
import winreg

from collector.base_collector import BaseCollector
from models.device import USBDevice
from utils.time_utils import TimeUtils


class USBRegistryCollector(BaseCollector):
    """
    Collects USB storage device artifacts from Windows Registry.

    Sources:

    SYSTEM\\CurrentControlSet\\Enum\\USBSTOR
        -> Device identity

    SYSTEM\\CurrentControlSet\\Enum\\USB
        -> ContainerID, DeviceDesc, FriendlyName
    """


    REGISTRY_PATH = r"SYSTEM\CurrentControlSet\Enum\USBSTOR"

    USB_ENUM_PATHS = [
    r"SYSTEM\CurrentControlSet\Enum\USBSTOR",
    r"SYSTEM\CurrentControlSet\Enum\USB"
]



    def collect(self):

        devices = []

        root = None
        usb_key = None


        try:

            root = winreg.ConnectRegistry(
                None,
                winreg.HKEY_LOCAL_MACHINE
            )


            usb_key = winreg.OpenKey(
                root,
                self.REGISTRY_PATH
            )


            vendor_count = winreg.QueryInfoKey(
                usb_key
            )[0]



            for i in range(vendor_count):

                vendor_product_name = winreg.EnumKey(
                    usb_key,
                    i
                )


                product_key = winreg.OpenKey(
                    usb_key,
                    vendor_product_name
                )


                instance_count = winreg.QueryInfoKey(
                    product_key
                )[0]



                for j in range(instance_count):

                    instance_name = winreg.EnumKey(
                        product_key,
                        j
                    )


                    if instance_name in [
                        "Device Parameters",
                        "Properties"
                    ]:
                        continue



                    full_path = (

                        self.REGISTRY_PATH
                        + "\\"
                        + vendor_product_name
                        + "\\"
                        + instance_name

                    )



                    timestamp = self.get_registry_timestamp(
                        product_key
                    )



                    manufacturer, product, revision = (

                        self.parse_device_name(
                            vendor_product_name
                        )

                    )



                    metadata = self.find_usb_metadata(
                        root,
                        instance_name
                    )



                    device = USBDevice(

                        manufacturer=manufacturer,

                        product=product,

                        revision=revision,

                        serial_number=instance_name,

                        registry_path=full_path,

                        last_connected=timestamp,

                        registry_timestamp=timestamp,

                        container_id=metadata["container_id"],

                        friendly_name=metadata["friendly_name"],

                        device_instance=metadata["device_instance"],

                        device_description=metadata["device_description"]

                    )



                    devices.append(device)



                    winreg.CloseKey(product_key)



        except Exception as error:

            print(
                "[Registry Collector Error]",
                error
            )



        finally:

            try:

                if usb_key:
                    winreg.CloseKey(
                        usb_key
                    )


                if root:
                    winreg.CloseKey(
                        root
                    )


            except Exception:

                pass



        return devices




    # =========================================================
    # SEARCH USB ENUM REGISTRY
    # =========================================================


    def find_usb_metadata(self, root, serial):

        metadata = {

            "container_id": "UNKNOWN",
            "friendly_name": "UNKNOWN",
            "device_description": "UNKNOWN",
            "device_instance": "UNKNOWN"

        }


        target = self.normalize_serial(serial).lower()


        for enum_path in self.USB_ENUM_PATHS:


            try:

                usb_root = winreg.OpenKey(
                    root,
                    enum_path
                )


                vendor_count = winreg.QueryInfoKey(
                    usb_root
                )[0]



                for i in range(vendor_count):


                    vendor = winreg.EnumKey(
                        usb_root,
                        i
                    )


                    vendor_key = winreg.OpenKey(
                        usb_root,
                        vendor
                    )


                    instance_count = winreg.QueryInfoKey(
                        vendor_key
                    )[0]



                    for j in range(instance_count):


                        instance = winreg.EnumKey(
                            vendor_key,
                            j
                        )


                        instance_key = winreg.OpenKey(
                            vendor_key,
                            instance
                        )


                        combined = (
                            vendor
                            +
                            "\\"
                            +
                            instance
                        ).lower()



                        if (

                            target in combined

                            or

                            serial.lower() in combined

                            or

                            self.normalize_serial(instance)
                            .lower()
                            in target

                        ):


                            metadata = self.read_metadata(

                                instance_key,

                                vendor,

                                instance

                            )


                            winreg.CloseKey(instance_key)
                            winreg.CloseKey(vendor_key)
                            winreg.CloseKey(usb_root)


                            return metadata



                        winreg.CloseKey(
                            instance_key
                        )


                    winreg.CloseKey(
                        vendor_key
                    )


                winreg.CloseKey(
                    usb_root
                )


            except Exception:

                continue



        return metadata





    # =========================================================
    # READ VALUES FROM USB ENUM DEVICE KEY
    # =========================================================


    def read_metadata(
            self,
            key,
            vendor,
            instance):


        metadata = {


            "container_id": "UNKNOWN",

            "friendly_name": "UNKNOWN",

            "device_description": "UNKNOWN",

            "hardware_id": "UNKNOWN",

            "device_instance":

                vendor + "\\" + instance

        }



        try:


            value_count = winreg.QueryInfoKey(

                key

            )[1]



            for i in range(value_count):


                name, value, _ = winreg.EnumValue(

                    key,

                    i

                )



                name_lower = name.lower()



                if name_lower == "containerid":

                    metadata["container_id"] = str(
                        value
                    )



                elif name_lower == "friendlyname":

                    metadata["friendly_name"] = str(
                        value
                    )



                elif name_lower == "devicedesc":

                    metadata["device_description"] = str(
                        value
                    )

                elif name_lower == "hardwareid":

                    metadata["hardware_id"] = str(value)



        except Exception:

            pass



        return metadata





    # =========================================================
    # SERIAL NORMALIZATION
    # =========================================================


    def normalize_serial(self, serial):

        serial = serial.replace(
            "_",
            ""
        )


        parts = serial.split("&")


        if len(parts) >= 2:

            return (
                parts[0]
                +
                "&"
                +
                parts[1]
            )


        return serial





    # =========================================================
    # DEVICE NAME PARSER
    # =========================================================


    def parse_device_name(
            self,
            name):


        manufacturer = "UNKNOWN"

        product = "UNKNOWN"

        revision = "UNKNOWN"



        parts = name.split("&")



        for part in parts:


            if part.startswith("Ven_"):

                manufacturer = part.replace(
                    "Ven_",
                    ""
                )



            elif part.startswith("Prod_"):

                product = part.replace(
                    "Prod_",
                    ""
                )



            elif part.startswith("Rev_"):

                revision = part.replace(
                    "Rev_",
                    ""
                )



        return (

            manufacturer,

            product,

            revision

        )





    # =========================================================
    # REGISTRY TIMESTAMP
    # =========================================================


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