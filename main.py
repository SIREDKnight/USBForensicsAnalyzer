from collector.registry import USBRegistryCollector
from reports.json_report import JSONReport


def banner():

    print("=" * 70)
    print("USB FORENSICS ANALYZER")
    print("=" * 70)


def main():

    banner()

    collector = USBRegistryCollector()

    devices = collector.get_devices()

    if not devices:

        print("No USB devices found.")
        return

    for number, device in enumerate(devices, start=1):

        print(f"\nUSB Device #{number}")
        print("-" * 70)
        print(device)

    JSONReport.save(devices)


if __name__ == "__main__":
    main()