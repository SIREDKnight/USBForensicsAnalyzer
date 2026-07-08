from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from utils.hash_utils import HashUtils


class PDFReport:

    OUTPUT_FILE = Path("output") / "case_report.pdf"

    @staticmethod
    def generate(
            case,
            devices,
            mounted,
            correlations,
            timeline):

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

        elements.append(Spacer(1, 20))

        # ==================================================
        # CASE INFORMATION
        # ==================================================

        elements.append(

            Paragraph(
                "CASE INFORMATION",
                styles["Heading1"]
            )

        )

        case_table = Table([

            ["Case ID", case[0]],
            ["Case Name", case[1]],
            ["Created", case[2]],
            ["Investigator", case[3]]

        ])

        case_table.setStyle(TableStyle([

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)

        ]))

        elements.append(case_table)

        elements.append(Spacer(1, 20))

        # ==================================================
        # EVIDENCE SUMMARY
        # ==================================================

        elements.append(

            Paragraph(
                "EVIDENCE SUMMARY",
                styles["Heading1"]
            )

        )

        summary = Table([

            ["Evidence Type", "Count"],

            ["USB Devices", len(devices)],

            ["Mounted Devices", len(mounted)],

            ["Timeline Events", len(timeline)],

            ["Correlations", len(correlations)]

        ])

        summary.setStyle(TableStyle([

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("ALIGN", (1, 1), (-1, -1), "CENTER")

        ]))

        elements.append(summary)

        elements.append(Spacer(1, 20))

        # ==================================================
        # USB DEVICES
        # ==================================================

        elements.append(

            Paragraph(
                "USB DEVICE DETAILS",
                styles["Heading1"]
            )

        )

        for device in devices:

            elements.append(

                Paragraph(

                    f"<b>Manufacturer:</b> {device.manufacturer}",

                    styles["Normal"]

                )

            )

            elements.append(

                Paragraph(

                    f"<b>Product:</b> {device.product}",

                    styles["Normal"]

                )

            )

            elements.append(

                Paragraph(

                    f"<b>Revision:</b> {device.revision}",

                    styles["Normal"]

                )

            )

            elements.append(

                Paragraph(

                    f"<b>Serial Number:</b> {device.serial_number}",

                    styles["Normal"]

                )

            )

            elements.append(

                Paragraph(

                    f"<b>Registry Path:</b> {device.registry_path}",

                    styles["Normal"]

                )

            )

            elements.append(

                Paragraph(

                    f"<b>SHA-256:</b> {HashUtils.sha256(device.to_dict())}",

                    styles["Code"]

                )

            )

            elements.append(Spacer(1, 15))

        # ==================================================
        # MOUNTED DEVICES
        # ==================================================

        elements.append(

            Paragraph(

                "MOUNTED DEVICE DETAILS",

                styles["Heading1"]

            )

        )

        for mount in mounted:

            elements.append(

                Paragraph(

                    f"<b>Drive Letter:</b> {mount.drive_letter}",

                    styles["Normal"]

                )

            )

            elements.append(

                Paragraph(

                    f"<b>Registry Name:</b> {mount.registry_name}",

                    styles["Normal"]

                )

            )

            elements.append(

                Paragraph(

                    f"<b>Volume GUID:</b> {mount.volume_guid}",

                    styles["Normal"]

                )

            )

            elements.append(

                Paragraph(

                    f"<b>SHA-256:</b> {HashUtils.sha256(mount.to_dict())}",

                    styles["Code"]

                )

            )

            elements.append(Spacer(1, 15))

        # ==================================================
        # TIMELINE
        # ==================================================

        elements.append(

            Paragraph(

                "FORENSIC TIMELINE",

                styles["Heading1"]

            )

        )

        timeline_table = [["Time", "Artifact", "Description"]]

        for event in timeline:

            timeline_table.append([

                event["time"],

                event["artifact"],

                event["description"]

            ])

        table = Table(timeline_table)

        table.setStyle(TableStyle([

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 6)

        ]))

        elements.append(table)

        elements.append(Spacer(1, 20))

        # ==================================================
        # CORRELATION ANALYSIS
        # ==================================================

        elements.append(

            Paragraph(

                "CORRELATION ANALYSIS",

                styles["Heading1"]

            )

        )

        for c in correlations:

            elements.append(

                Paragraph(

                    f"<b>Device:</b> {c['product']}",

                    styles["Normal"]

                )

            )

            elements.append(

                Paragraph(

                    f"<b>Manufacturer:</b> {c['manufacturer']}",

                    styles["Normal"]

                )

            )

            elements.append(

                Paragraph(

                    f"<b>Drive Letter:</b> {c['drive_letter']}",

                    styles["Normal"]

                )

            )

            elements.append(

                Paragraph(

                    f"<b>Confidence:</b> {c['confidence']}%",

                    styles["Normal"]

                )

            )

            elements.append(

                Paragraph(

                    "<b>Supporting Evidence</b>",

                    styles["Heading3"]

                )

            )

            for reason in c["reasons"]:

                elements.append(

                    Paragraph(

                        f"• {reason}",

                        styles["Normal"]

                    )

                )

            elements.append(Spacer(1, 15))

        # ==================================================
        # CONCLUSION
        # ==================================================

        elements.append(

            Paragraph(

                "CONCLUSION",

                styles["Heading1"]

            )

        )

        conclusion = """
        This report summarizes USB device activity identified on the
        examined Windows system. Evidence was acquired from Registry
        artifacts, MountedDevices entries, and Windows Event Logs.

        Correlation analysis was performed using weighted evidence
        scoring, and all collected artifacts were verified using
        SHA-256 hashing to preserve forensic integrity.

        This report was generated automatically by the
        USB Forensics Analyzer.
        """

        elements.append(

            Paragraph(

                conclusion,

                styles["Normal"]

            )

        )

        doc.build(elements)

        print(

            f"\n[+] PDF report generated: {PDFReport.OUTPUT_FILE}"

        )