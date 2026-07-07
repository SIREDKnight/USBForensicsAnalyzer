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
    print("4. View timeline")
    print("5. View correlations")
    print("6. Export case bundle")
    print("7. Exit")



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



        # ==========================================
        # FULL ACQUISITION
        # ==========================================

        if choice == "1":


            (

                devices,

                mounted,

                correlations,

                timeline

            ) = manager.collect()



            print(

                "\n[+] Acquisition completed successfully"

            )


            print(

                f"Devices     : {len(devices)}"

            )


            print(

                f"Mounted     : {len(mounted)}"

            )


            print(

                f"Correlations: {len(correlations)}"

            )




        # ==========================================
        # PDF REPORT
        # ==========================================

        elif choice == "2":


            report_path = Path(

                "output"

            ) / "case_report.pdf"



            if report_path.exists():


                print(

                    "\nOpening PDF report..."

                )


                os.startfile(

                    report_path

                )


            else:


                print(

                    "\n[-] No report found. Run acquisition first."

                )




        # ==========================================
        # DEVICE QUERY
        # ==========================================

        elif choice == "3":


            serial = input(

                "Enter serial number: "

            )



            device, device_timeline = manager.query_device(

                serial

            )



            if device:


                print("\nDEVICE DETAILS")

                print("=" * 70)


                print(

                    device

                )


                print("\nTIMELINE")

                print("=" * 70)



                for event in device_timeline:


                    print(event)



            else:


                print(

                    "Device not found."

                )




        # ==========================================
        # TIMELINE VIEW
        # ==========================================

        elif choice == "4":


            print("\nFORENSIC TIMELINE")

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




        # ==========================================
        # CORRELATIONS VIEW
        # ==========================================

        elif choice == "5":


            print("\nFORENSIC CORRELATIONS")

            print("=" * 70)



            if correlations:


                for c in correlations:



                    print("\n" + "-" * 70)



                    print(

                        f"Device      : {c['product']}"

                    )


                    print(

                        f"Manufacturer: {c['manufacturer']}"

                    )


                    print(

                        f"Drive       : {c['drive_letter']}"

                    )


                    print(

                        f"Confidence  : {c['confidence']}%"

                    )


                    print("\nReasons:")



                    for reason in c["reasons"]:


                        print(

                            f"- {reason}"

                        )



            else:


                print(

                    "No correlations found."

                )




        # ==========================================
        # EXPORT CASE
        # ==========================================

        elif choice == "6":


            manager.export_case()




        # ==========================================
        # EXIT
        # ==========================================

        elif choice == "7":


            manager.close()


            print(

                "\nExiting USB Forensics Analyzer..."

            )


            break



        else:


            print(

                "Invalid option. Try again."

            )




if __name__ == "__main__":

    main()