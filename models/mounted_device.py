from dataclasses import dataclass, asdict


@dataclass
class MountedDevice:
    """
    Represents a mounted storage device artifact.

    Stores Windows MountedDevices registry information
    used for drive mapping and forensic analysis.
    """

    drive_letter: str

    registry_name: str

    volume_guid: str

    registry_timestamp: str = "UNKNOWN"


    # ==================================================
    # Enhanced forensic identifiers
    # ==================================================

    device_identifier: str = "UNKNOWN"

    volume_serial: str = "UNKNOWN"



    def to_dict(self):
        """
        Convert object into dictionary format
        for JSON reports and database storage.
        """

        return asdict(self)



    def __str__(self):

        return (

            "\nMOUNTED DEVICE\n"

            "-------------------------\n"

            f"Drive Letter       : {self.drive_letter}\n"

            f"Registry Name      : {self.registry_name}\n"

            f"Volume GUID        : {self.volume_guid}\n"

            f"Registry Timestamp : {self.registry_timestamp}\n"

            f"Device Identifier  : {self.device_identifier}\n"

            f"Volume Serial      : {self.volume_serial}\n"

        )