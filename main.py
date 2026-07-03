from manager.evidence_manager import EvidenceManager


def banner():

    print("=" * 70)
    print("USB FORENSICS ANALYZER")
    print("=" * 70)


def main():

    banner()

    manager = EvidenceManager()

    devices, mounted, correlations, timeline = manager.collect()

    # -------------------------
    # USB DEVICES
    # -------------------------
    print("\nUSB DEVICES")
    print("=" * 70)

    for number, device in enumerate(devices, start=1):

        print(f"\nUSB Device #{number}")
        print("-" * 70)
        print(device)

    # -------------------------
    # MOUNTED DEVICES
    # -------------------------
    print("\nMOUNTED DEVICES")
    print("=" * 70)

    for item in mounted:

        print(item)
        print("-" * 70)

    # -------------------------
    # CORRELATIONS
    # -------------------------
    print("\nCORRELATIONS")
    print("=" * 70)

    if correlations:

        for c in correlations:

            print(f"Serial Number : {c['serial_number']}")
            print(f"Drive Letter  : {c['drive_letter']}")
            print(f"Product       : {c['product']}")
            print("-" * 70)

    else:
        print("No correlations found.")

    # -------------------------
    # FORENSIC TIMELINE
    # -------------------------
    print("\nFORENSIC TIMELINE")
    print("=" * 70)

    for event in timeline:

        print(f"{event['event_time']} | {event['artifact']} | {event['description']}")
        print("-" * 70)

    manager.close()


if __name__ == "__main__":
    main()