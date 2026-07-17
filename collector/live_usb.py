import wmi

from collector.base_collector import BaseCollector


class LiveUSBCollector(BaseCollector):

    def collect(self):

        results = []

        c = wmi.WMI()

        for disk in c.Win32_DiskDrive():

            if "USBSTOR" not in disk.PNPDeviceID.upper():
                continue

            drive_letters = []

            for partition in disk.associators(
                "Win32_DiskDriveToDiskPartition"
            ):

                for logical in partition.associators(
                    "Win32_LogicalDiskToPartition"
                ):

                    drive_letters.append(
                        logical.DeviceID
                    )

            results.append({

                "friendly_name": disk.Caption,

                "instance_id": disk.PNPDeviceID,

                "physical_drive": disk.DeviceID,

                "drive_letters": drive_letters

            })

        return results