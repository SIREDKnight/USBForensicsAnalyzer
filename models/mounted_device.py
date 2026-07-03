from dataclasses import dataclass

@dataclass
class MountedDevice:
    drive_letter: str
    registry_name: str

    # NEW FIELD (for correlation)
    volume_guid: str = None

    def __str__(self):
        return (
            f"Drive Letter : {self.drive_letter}\n"
            f"Registry Name: {self.registry_name}\n"
            f"Volume GUID  : {self.volume_guid}"
        )