from pathlib import Path
import os

from manager.evidence_manager import EvidenceManager



def banner():

    print("=" * 70)

    print("        USB FORENSICS ANALYZER - DFIR EDITION")

    print("=" * 70)



def menu():

    print()

    print("=" * 70)

    print("FORENSIC MENU")

    print("=" * 70)

    print("[1] Run Full Acquisition")

    print("[2] Open PDF Report")

    print("[3] Query Device By Serial Number")

    print("[4] View Timeline")

    print("[5] View Correlations")

    print("[6] Export Case Bundle")

    print("[7] Exit")

    print("=" * 70)



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



        # ==================================================
        # ACQUISITION
        # ==================================================

        if choice == "1":


            try:


                (

                    devices,

                    mounted,

                    correlations,

                    timeline

                ) = manager.collect()



                print()

                print("=" * 70)

                print("ACQUISITION COMPLETED")

                print("=" * 70)

                print(
                    f"USB Devices      : {len(devices)}"
                )

                print(
                    f"Mounted Devices  : {len(mounted)}"
                )

                print(
                    f"Timeline Events  : {len(timeline)}"
                )

                print(
                    f"Correlations     : {len(correlations)}"
                )

                print("=" * 70)



            except Exception as error:


                print()

                print("[ERROR] Acquisition failed")

                print(error)



        # ==================================================
        # PDF REPORT
        # ==================================================

        elif choice == "2":


            report = Path(

                "output"

            ) / "case_report.pdf"



            if report.exists():


                print(

                    "\nOpening PDF report..."

                )


                os.startfile(

                    report

                )


            else:


                print(

                    "\n[-] Report not found. Run acquisition first."

                )



        # ==================================================
        # DEVICE QUERY
        # ==================================================

        elif choice == "3":


            serial = input(

                "\nEnter serial number: "

            )


            device, device_timeline = manager.query_device(

                serial

            )


            if device:


                print()

                print("=" * 70)

                print("DEVICE INFORMATION")

                print("=" * 70)


                print(

                    dict(device)

                )


                print()

                print("TIMELINE")

                print("=" * 70)



                for event in device_timeline:


                    print(

                        event

                    )



            else:


                print(

                    "\n[-] Device not found."

                )



        # ==================================================
        # TIMELINE
        # ==================================================

        elif choice == "4":


            print()

            print("=" * 70)

            print("FORENSIC TIMELINE")

            print("=" * 70)



            if timeline:


                for event in timeline:


                    print(

                        f"{event['time']} | "

                        f"{event['artifact']} | "

                        f"{event['description']}"

                    )


            else:


                print(

                    "No timeline available. Run acquisition first."

                )



        # ==================================================
        # CORRELATIONS
        # ==================================================

        elif choice == "5":


            print()

            print("=" * 70)

            print("FORENSIC CORRELATIONS")

            print("=" * 70)



            if correlations:


                for item in correlations:


                    print()

                    print("-" * 70)


                    print(

                        f"Device       : {item['product']}"

                    )


                    print(

                        f"Manufacturer : {item['manufacturer']}"

                    )


                    print(

                        f"Drive        : {item['drive_letter']}"

                    )


                    print(

                        f"Confidence   : {item['confidence']}%"

                    )


                    print()

                    print("Supporting Evidence:")



                    for reason in item["reasons"]:


                        print(

                            f" - {reason}"

                        )



            else:


                print(

                    "No correlations found."

                )



        # ==================================================
        # EXPORT
        # ==================================================

        elif choice == "6":


            manager.export_case()



        # ==================================================
        # EXIT
        # ==================================================

        elif choice == "7":


            manager.close()


            print()

            print(

                "Exiting USB Forensics Analyzer..."

            )


            break



        else:


            print(

                "Invalid option."

            )




if __name__ == "__main__":

    main()