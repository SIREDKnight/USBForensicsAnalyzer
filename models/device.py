from dataclasses import dataclass

@dataclass
class USBDevice:
    manufacturer: str
    product: str
    revision: str
    serial_number: str
    registry_path: str

    def __str__(self):
        return (
            f"Manufacturer : {self.manufacturer}\n"
            f"Product      : {self.product}\n"
            f"Revision     : {self.revision}\n"
            f"Serial No.   : {self.serial_number}\n"
            f"Registry Path: {self.registry_path}"
        )