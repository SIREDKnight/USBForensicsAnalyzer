from pathlib import Path

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet



class PDFReport:


    OUTPUT_FILE = Path("output") / "case_report.pdf"



    @staticmethod
    def generate(
            case,
            devices,
            mounted,
            correlations,
            timeline):


        PDFReport.OUTPUT_FILE.parent.mkdir(
            exist_ok=True
        )


        doc = SimpleDocTemplate(

            str(PDFReport.OUTPUT_FILE)

        )


        styles = getSampleStyleSheet()


        elements = []



        # ==================================================
        # TITLE
        # ==================================================

        elements.append(

            Paragraph(
                "USB FORENSICS CASE REPORT",
                styles["Title"]
            )

        )


        elements.append(

            Spacer(1, 20)

        )



        # ==================================================
        # CASE INFORMATION
        # ==================================================

        elements.append(

            Paragraph(
                "CASE INFORMATION",
                styles["Heading2"]
            )

        )


        if case:


            elements.append(

                Paragraph(
                    f"Case ID: {case[0]}",
                    styles["Normal"]
                )

            )


            elements.append(

                Paragraph(
                    f"Case Name: {case[1]}",
                    styles["Normal"]
                )

            )


            elements.append(

                Paragraph(
                    f"Created: {case[2]}",
                    styles["Normal"]
                )

            )


            elements.append(

                Paragraph(
                    f"Investigator: {case[3]}",
                    styles["Normal"]
                )

            )



        elements.append(

            Spacer(1, 15)

        )




        # ==================================================
        # USB DEVICES
        # ==================================================

        elements.append(

            Paragraph(
                "USB DEVICES",
                styles["Heading2"]
            )

        )


        if devices:


            for device in devices:


                elements.append(

                    Paragraph(

                        (
                            f"Manufacturer: {device.manufacturer}<br/>"
                            f"Product: {device.product}<br/>"
                            f"Revision: {device.revision}<br/>"
                            f"Serial Number: {device.serial_number}<br/>"
                            f"Registry Path: {device.registry_path}"
                        ),

                        styles["Normal"]

                    )

                )


                elements.append(

                    Spacer(1,10)

                )


        else:

            elements.append(

                Paragraph(
                    "No USB devices detected.",
                    styles["Normal"]
                )

            )




        # ==================================================
        # MOUNTED DEVICES
        # ==================================================

        elements.append(

            Paragraph(
                "MOUNTED DEVICES",
                styles["Heading2"]
            )

        )


        if mounted:


            for mount in mounted:


                elements.append(

                    Paragraph(

                        (
                            f"Drive Letter: {mount.drive_letter}<br/>"
                            f"Registry Name: {mount.registry_name}<br/>"
                            f"Volume GUID: {mount.volume_guid}"
                        ),

                        styles["Normal"]

                    )

                )


                elements.append(

                    Spacer(1,10)

                )


        else:

            elements.append(

                Paragraph(
                    "No mounted devices detected.",
                    styles["Normal"]
                )

            )




        # ==================================================
        # TIMELINE
        # ==================================================

        elements.append(

            Paragraph(
                "FORENSIC TIMELINE",
                styles["Heading2"]
            )

        )


        if timeline:


            for event in timeline:


                elements.append(

                    Paragraph(

                        (
                            f"{event['time']} | "
                            f"{event['artifact']} | "
                            f"{event['description']}"
                        ),

                        styles["Normal"]

                    )

                )


        else:


            elements.append(

                Paragraph(
                    "No timeline events available.",
                    styles["Normal"]
                )

            )




        # ==================================================
        # CORRELATIONS
        # ==================================================

        elements.append(

            Paragraph(
                "CORRELATION FINDINGS",
                styles["Heading2"]
            )

        )


        if correlations:


            for item in correlations:


                elements.append(

                    Paragraph(

                        (
                            f"Device: {item.get('product')}<br/>"
                            f"Manufacturer: {item.get('manufacturer')}<br/>"
                            f"Drive: {item.get('drive_letter')}<br/>"
                            f"Confidence: {item.get('confidence')}%<br/>"
                            f"Reasons: {', '.join(item.get('reasons', []))}"
                        ),

                        styles["Normal"]

                    )

                )


                elements.append(

                    Spacer(1,10)

                )


        else:


            elements.append(

                Paragraph(
                    "No correlation findings.",
                    styles["Normal"]
                )

            )




        # ==================================================
        # CONCLUSION
        # ==================================================

        elements.append(

            Spacer(1,20)

        )


        elements.append(

            Paragraph(
                "CONCLUSION",
                styles["Heading2"]
            )

        )


        elements.append(

            Paragraph(

                (
                    "This report summarizes collected USB forensic "
                    "artifacts including device identification, "
                    "mounted drive evidence, Windows event activity, "
                    "timeline reconstruction and correlation analysis."
                ),

                styles["Normal"]

            )

        )



        doc.build(elements)



        print(

            f"\n[+] PDF report generated: {PDFReport.OUTPUT_FILE}"

        )