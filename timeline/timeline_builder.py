from models.timeline_event import TimelineEvent


class TimelineBuilder:
    """
    Builds an activity-based forensic timeline.

    Sources:
    - USB Registry
    - Mounted Devices
    - Windows Event Logs
    """

    EVENT_MAP = {

        10000: (
            "USB_OPERATIONAL",
            "USB device became operational"
        ),

        10001: (
            "USB_STARTED",
            "USB device started"
        ),

        10002: (
            "USB_STOPPED",
            "USB device stopped"
        ),

        10100: (
            "USB_DRIVER",
            "Windows loaded the USB device driver"
        ),

        20003: (
            "USB_PNP",
            "Plug-and-Play detected a USB device"
        ),

        225: (
            "USB_KERNEL",
            "Kernel Plug-and-Play processed a USB device"
        )

    }

    def build(
            self,
            devices,
            mounted_devices,
            event_logs
    ):

        timeline = []

        # ==================================================
        # USB DEVICES
        # ==================================================

        for device in devices:

            name = (
                device.friendly_name
                if device.friendly_name != "UNKNOWN"
                else f"{device.manufacturer} {device.product}"
            )

            timeline.append(

                TimelineEvent(

                    time=device.last_connected,

                    artifact="USB_CONNECTED",

                    description=(
                        f"USB device '{name}' "
                        f"was recorded in the Windows Registry "
                        f"(Serial: {device.serial_number})"
                    ),

                    source="Windows Registry",

                    event_id=None

                )

            )

        # ==================================================
        # MOUNTED DEVICES
        # ==================================================

        for mount in mounted_devices:

            timeline.append(

                TimelineEvent(

                    time=mount.registry_timestamp,

                    artifact="DRIVE_ASSIGNED",

                    description=(

                        f"Drive letter {mount.drive_letter} "

                        f"assigned "

                        f"(Volume: {mount.volume_guid})"

                    ),

                    source="Windows Registry",

                    event_id=None

                )

            )

        # ==================================================
        # EVENT LOGS
        # ==================================================

        for event in event_logs:

            event_id = event.get("event_id")

            artifact, description = self.EVENT_MAP.get(

                event_id,

                (

                    "EVENT_LOG",

                    event.get(

                        "description",

                        "USB related Windows event"

                    )

                )

            )

            timeline.append(

                TimelineEvent(

                    time=event.get(

                        "time",

                        "UNKNOWN"

                    ),

                    artifact=artifact,

                    description=description,

                    event_id=event_id,

                    source=event.get(

                        "source",

                        "Windows Event Log"

                    )

                )

            )

        # ==================================================
        # NORMALIZE
        # ==================================================

        for event in timeline:

            event.normalize_time()

        # ==================================================
        # SORT
        # ==================================================

        timeline.sort(

            key=lambda x:

            x.time

            if x.time != "UNKNOWN"

            else "9999-12-31 23:59:59"

        )

        return timeline