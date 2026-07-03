from collector.registry import USBRegistryCollector
from reports.json_report import JSONReport
from database.database import EvidenceDatabase

def banner():

    print("=" * 70)
    print("USB FORENSICS ANALYZER")
    print("=" * 70)


def main():

    banner()

    collector = USBRegistryCollector()
    database = EvidenceDatabase()

    devices = collector.get_devices()

    if not devices:

        print("No USB devices found.")
        return

    for number, device in enumerate(devices, start=1):

        database.insert_device(device)

        print(f"\nUSB Device #{number}")
        print("-" * 70)
        print(device)

    JSONReport.save(devices)
    database.close()


if __name__ == "__main__":
    main()