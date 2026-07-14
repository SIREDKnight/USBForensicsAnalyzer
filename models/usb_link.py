class USBLink:
    """
    Represents a Windows USB enumeration artifact that links
    a USB device to its Container ID and other identifiers.

    This model is used by the correlation engine to associate
    USBSTOR entries with mounted drives.
    """

    def __init__(
            self,
            serial_number,
            container_id,
            friendly_name,
            device_instance_id,
            parent_id_prefix
    ):

        self.serial_number = serial_number or "UNKNOWN"

        self.container_id = container_id or "UNKNOWN"

        self.friendly_name = friendly_name or "UNKNOWN"

        self.device_instance_id = device_instance_id or "UNKNOWN"

        self.parent_id_prefix = parent_id_prefix or "UNKNOWN"

    def to_dict(self):

        return {

            "serial_number": self.serial_number,

            "container_id": self.container_id,

            "friendly_name": self.friendly_name,

            "device_instance_id": self.device_instance_id,

            "parent_id_prefix": self.parent_id_prefix

        }

    def __str__(self):

        return (
            f"{self.friendly_name} | "
            f"{self.serial_number} | "
            f"{self.container_id}"
        )