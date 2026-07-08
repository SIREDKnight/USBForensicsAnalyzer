from dataclasses import dataclass


@dataclass
class USBDevice:
    """
    Represents a USB device artifact collected from Windows registry.
    """

    manufacturer: str

    product: str

    revision: str

    serial_number: str

    registry_path: str

    registry_time: str = "UNKNOWN"



    def to_dict(self):
        """
        Convert object into dictionary format
        for JSON reports and database storage.
        """

        return {

            "manufacturer":
            self.manufacturer,


            "product":
            self.product,


            "revision":
            self.revision,


            "serial_number":
            self.serial_number,


            "registry_path":
            self.registry_path,


            "registry_time":
            self.registry_time

        }



    def __str__(self):

        return (

            "\nUSB DEVICE\n"
            "-------------------------\n"

            f"Manufacturer : {self.manufacturer}\n"

            f"Product      : {self.product}\n"

            f"Revision     : {self.revision}\n"

            f"Serial No.   : {self.serial_number}\n"

            f"Registry Path: {self.registry_path}\n"

            f"Registry Time: {self.registry_time}\n"

        )