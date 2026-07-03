from dataclasses import dataclass


@dataclass
class MountedDevice:
    drive_letter: str
    registry_name: str

    def __str__(self):
        return (
            f"Drive Letter : {self.drive_letter}\n"
            f"Registry Name: {self.registry_name}"
        )