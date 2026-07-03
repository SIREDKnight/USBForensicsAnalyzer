from pathlib import Path
import os

from manager.evidence_manager import EvidenceManager


def banner():

    print("=" * 70)
    print("USB FORENSICS ANALYZER - DFIR EDITION")
    print("=" * 70)


def menu():

    print("\nFORENSIC MENU")
    print("=" * 70)
    print("1. Run full acquisition")
    print("2. View PDF report")
    print("3. Query device by serial")
    print("4. View forensic timeline")
    print("5. Export case bundle")
    print("6. Exit")


def main():

    banner()

    manager = EvidenceManager()

    timeline = []

    while True:

        menu()

        choice = input("\nSelect option: ")

        # -------------------------------------------------
        # 1. RUN ACQUISITION
        # -------------------------------------------------
        if choice == "1":

            devices, mounted, correlations, timeline = manager.collect()

            print("\n[+] Acquisition completed successfully.")
            print(f"USB Devices      : {len(devices)}")
            print(f"Mounted Devices  : {len(mounted)}")
            print(f"Correlations     : {len(correlations)}")

        # -------------------------------------------------
        # 2. VIEW PDF REPORT
        # -------------------------------------------------
        elif choice == "2":

            report = Path("output") / "case_report.pdf"

            if report.exists():

                print("\nOpening PDF report...")

                os.startfile(report)

            else:

                print("\nNo PDF report found.")
                print("Run acquisition first.")

        # -------------------------------------------------
        # 3. QUERY DEVICE
        # -------------------------------------------------
        elif choice == "3":

            serial = input("\nEnter USB serial number: ")

            device, device_timeline = manager.query_device(serial)

            print("\nDEVICE INFORMATION")
            print("=" * 70)

            if device:

                print(f"Manufacturer : {device[0]}")
                print(f"Product      : {device[1]}")
                print(f"Revision     : {device[2]}")
                print(f"Serial No.   : {device[3]}")
                print(f"Registry Path: {device[4]}")

                print("\nTIMELINE")
                print("=" * 70)

                if device_timeline:

                    for event in device_timeline:

                        print(f"{event[0]} | {event[1]} | {event[2]}")

                else:

                    print("No timeline events found.")

            else:

                print("Device not found.")

        # -------------------------------------------------
        # 4. VIEW TIMELINE
        # -------------------------------------------------
        elif choice == "4":

            print("\nFORENSIC TIMELINE")
            print("=" * 70)

            if timeline:

                for event in timeline:

                    print(f"{event[0]} | {event[1]} | {event[2]}")

            else:

                print("Timeline is empty.")
                print("Run acquisition first.")

        # -------------------------------------------------
        # 5. EXPORT CASE
        # -------------------------------------------------
        elif choice == "5":

            manager.export_case()

        # -------------------------------------------------
        # 6. EXIT
        # -------------------------------------------------
        elif choice == "6":

            manager.close()

            print("\nExiting USB Forensics Analyzer...")

            break

        else:

            print("\nInvalid option. Please try again.")


if __name__ == "__main__":
    main()