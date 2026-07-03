from manager.evidence_manager import EvidenceManager


def banner():

    print("=" * 70)
    print("USB FORENSICS ANALYZER - DFIR EDITION")
    print("=" * 70)


def main():

    banner()

    manager = EvidenceManager()

    # -------------------------
    # COLLECTION PHASE
    # -------------------------
    devices, mounted, correlations, timeline = manager.collect()

    # -------------------------
    # CASE INFO
    # -------------------------
    case = manager.database.get_latest_case()

    print("\nFORENSIC CASE INFO")
    print("=" * 70)

    if case:
        print(f"Case ID      : {case[0]}")
        print(f"Case Name    : {case[1]}")
        print(f"Created At   : {case[2]}")
        print(f"Investigator : {case[3]}")
    else:
        print("No case found")

    # -------------------------
    # USB DEVICES
    # -------------------------
    print("\nUSB DEVICES")
    print("=" * 70)

    for i, device in enumerate(devices, start=1):

        print(f"\nDevice #{i}")
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
    # CORRELATIONS (WITH CONFIDENCE)
    # -------------------------
    print("\nCORRELATIONS (WITH CONFIDENCE)")
    print("=" * 70)

    if correlations:

        for c in correlations:

            print(f"Serial Number : {c['serial_number']}")
            print(f"Drive Letter  : {c['drive_letter']}")
            print(f"Product       : {c['product']}")
            print(f"Confidence    : {c['confidence']}%")
            print("-" * 70)

    else:
        print("No correlations found.")

    # -------------------------
    # FORENSIC TIMELINE
    # -------------------------
    print("\nFORENSIC TIMELINE")
    print("=" * 70)

    for event in timeline:

        print(f"{event[0]} | {event[1]} | {event[2]}")
        print("-" * 70)

    # -------------------------
    # FORENSIC QUERY ENGINE DEMO
    # -------------------------
    print("\nFORENSIC QUERY ENGINE DEMO")
    print("=" * 70)

    if devices:

        serial = devices[0].serial_number

        device, usb_timeline = manager.query_device(serial)

        print("\nDEVICE LOOKUP RESULT")
        print("-" * 70)

        if device:
            print(f"Manufacturer : {device[0]}")
            print(f"Product      : {device[1]}")
            print(f"Revision     : {device[2]}")
            print(f"Serial       : {device[3]}")
            print(f"Registry Path: {device[4]}")
        else:
            print("Device not found")

        print("\nDEVICE TIMELINE")
        print("-" * 70)

        for t in usb_timeline:

            print(f"{t[0]} | {t[1]} | {t[2]}")
            print("-" * 70)

    manager.close()


if __name__ == "__main__":
    main()