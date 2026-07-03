from manager.evidence_manager import EvidenceManager


def banner():

    print("=" * 70)
    print("USB FORENSICS ANALYZER")
    print("=" * 70)


def main():

    banner()

    manager = EvidenceManager()

    devices, mounted = manager.collect()

    for number, device in enumerate(devices, start=1):

        print(f"\nUSB Device #{number}")
        print("-" * 70)
        print(device)

        print("\nMounted Devices")
        print("=" * 70)

        for item in mounted:
          print(item)
          print("-" * 70)

    manager.close()


if __name__ == "__main__":
    main()