from dataclasses import dataclass, asdict


@dataclass
class USBDevice:
    """
    Represents a USB device artifact collected from Windows registry.

    Stores identifying information and forensic metadata.
    """

    manufacturer: str

    product: str

    revision: str

    serial_number: str

    registry_path: str

    last_connected: str = "UNKNOWN"

    registry_timestamp: str = "UNKNOWN"


    # ==================================================
    # Enhanced forensic identifiers
    # ==================================================

    container_id: str = "UNKNOWN"

    friendly_name: str = "UNKNOWN"

    device_instance: str = "UNKNOWN"

    device_description: str = "UNKNOWN"



    def to_dict(self):
        """
        Convert object into dictionary format
        for JSON reports and database storage.
        """

        return asdict(self)



    def __str__(self):

        return (

            "\nUSB DEVICE\n"

            "-------------------------\n"

            f"Manufacturer       : {self.manufacturer}\n"

            f"Product            : {self.product}\n"

            f"Revision           : {self.revision}\n"

            f"Serial No.         : {self.serial_number}\n"

            f"Registry Path      : {self.registry_path}\n"

            f"Last Connected     : {self.last_connected}\n"

            f"Registry Timestamp : {self.registry_timestamp}\n"

            f"Container ID       : {self.container_id}\n"

            f"Friendly Name      : {self.friendly_name}\n"

            f"Device Instance    : {self.device_instance}\n"

            f"Description        : {self.device_description}\n"

        )