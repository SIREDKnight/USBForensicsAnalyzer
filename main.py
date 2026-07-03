from manager.evidence_manager import EvidenceManager


def banner():

    print("=" * 70)
    print("USB FORENSICS ANALYZER - INTERACTIVE MODE")
    print("=" * 70)


def menu():

    print("\nFORENSIC MENU")
    print("=" * 70)
    print("1. Run full acquisition")
    print("2. View forensic PDF report")
    print("3. Query device by serial")
    print("4. View full timeline")
    print("5. Exit")


def main():

    banner()

    manager = EvidenceManager()

    devices = []
    mounted = []
    correlations = []
    timeline = []

    while True:

        menu()

        choice = input("\nSelect option: ")

        # -------------------------
        # 1. RUN ACQUISITION
        # -------------------------
        if choice == "1":

            devices, mounted, correlations, timeline = manager.collect()

            print("\n[+] Acquisition complete")
            print(f"[+] Devices: {len(devices)}")
            print(f"[+] Mounted: {len(mounted)}")
            print(f"[+] Correlations: {len(correlations)}")

        # -------------------------
        # 2. VIEW PDF REPORT
        # -------------------------
        elif choice == "2":

            from pathlib import Path
            import os

            report_path = Path("output/case_report.pdf")

            if report_path.exists():

                print("\n[+] Opening forensic PDF report...")

                os.startfile(report_path)

            else:

                print("\n[-] No PDF report found. Run option 1 first.")

        # -------------------------
        # 3. QUERY DEVICE
        # -------------------------
        elif choice == "3":

            serial = input("Enter serial number: ")

            device, device_timeline = manager.query_device(serial)

            print("\n[DEVICE RESULT]")
            print("=" * 70)

            if device:
                print(f"Manufacturer : {device[0]}")
                print(f"Product      : {device[1]}")
                print(f"Revision     : {device[2]}")
                print(f"Serial       : {device[3]}")
                print(f"Registry Path: {device[4]}")
            else:
                print("Device not found")

            print("\n[TIMELINE]")
            print("=" * 70)

            for t in device_timeline:
                print(f"{t[0]} | {t[1]} | {t[2]}")

        # -------------------------
        # 4. FULL TIMELINE
        # -------------------------
        elif choice == "4":

            print("\n[FULL FORENSIC TIMELINE]")
            print("=" * 70)

            if not timeline:
                print("No timeline available. Run acquisition first.")
            else:
                for event in timeline:
                    print(f"{event[0]} | {event[1]} | {event[2]}")

        # -------------------------
        # 5. EXIT
        # -------------------------
        elif choice == "5":

            manager.close()
            print("\n[+] Exiting forensic tool...")
            break

        else:

            print("\n[-] Invalid option")


if __name__ == "__main__":
    main()