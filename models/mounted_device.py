from dataclasses import dataclass


@dataclass
class MountedDevice:
    """
    Represents a Windows mounted device artifact.
    Collected from SYSTEM\\MountedDevices registry key.
    """

    drive_letter: str
    registry_name: str
    volume_guid: str = None


    def to_dict(self):
        """
        Convert object into dictionary format
        for JSON/PDF reports and database storage.
        """

        return {
            "drive_letter": self.drive_letter,
            "registry_name": self.registry_name,
            "volume_guid": self.volume_guid
        }


    def __str__(self):

        return (
            "\nMOUNTED DEVICE\n"
            "-------------------------\n"
            f"Drive Letter : {self.drive_letter}\n"
            f"Registry Name: {self.registry_name}\n"
            f"Volume GUID  : {self.volume_guid}\n"
        )