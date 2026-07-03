from manager.evidence_manager import EvidenceManager


def banner():
    print("=" * 70)
    print("USB FORENSICS ANALYZER")
    print("=" * 70)


def main():

    banner()

    manager = EvidenceManager()

    devices, mounted, correlations = manager.collect()

    # -------------------------
    # USB Devices Output
    # -------------------------
    for number, device in enumerate(devices, start=1):

        print(f"\nUSB Device #{number}")
        print("-" * 70)
        print(device)

    # -------------------------
    # Mounted Devices Output
    # -------------------------
    print("\nMounted Devices")
    print("=" * 70)

    for item in mounted:

        print(item)
        print("-" * 70)

    # -------------------------
    # Correlation Output
    # -------------------------
    print("\nCorrelations")
    print("=" * 70)

    if correlations:

        for c in correlations:
            print(f"Serial Number : {c['serial_number']}")
            print(f"Drive Letter  : {c['drive_letter']}")
            print(f"Product       : {c['product']}")
            print("-" * 70)

    else:
        print("No correlations found.")

    manager.close()


if __name__ == "__main__":
    main()