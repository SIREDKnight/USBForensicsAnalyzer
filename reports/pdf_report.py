from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

from utils.hash_utils import HashUtils



class PDFReport:


    OUTPUT_FILE = Path("output") / "case_report.pdf"



    @staticmethod
    def add_footer(canvas, doc):

        canvas.saveState()

        canvas.setFont(
            "Helvetica",
            8
        )

        canvas.drawString(
            40,
            25,
            "USB Forensics Analyzer - DFIR Investigation Report"
        )

        canvas.drawRightString(
            550,
            25,
            f"Page {doc.page}"
        )

        canvas.restoreState()



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



        document = SimpleDocTemplate(

            str(PDFReport.OUTPUT_FILE),

            pagesize=A4

        )



        styles = getSampleStyleSheet()

        elements = []



        # ==================================================
        # COVER PAGE
        # ==================================================

        cover_title = ParagraphStyle(

            "CoverTitle",

            parent=styles["Title"],

            alignment=TA_CENTER,

            fontSize=24

        )



        cover_text = ParagraphStyle(

            "CoverText",

            parent=styles["Normal"],

            alignment=TA_CENTER,

            fontSize=12,

            leading=18

        )



        elements.append(

            Spacer(1,100)

        )


        elements.append(

            Paragraph(

                "USB FORENSICS ANALYZER",

                cover_title

            )

        )


        elements.append(

            Paragraph(

                "FORENSIC INVESTIGATION REPORT",

                cover_title

            )

        )


        elements.append(

            Spacer(1,40)

        )



        elements.append(

            Paragraph(

                f"""

                <b>Case ID:</b><br/>

                {case['case_id']}

                <br/><br/>

                <b>Case Name:</b><br/>

                {case['case_name']}

                <br/><br/>

                <b>Investigator:</b><br/>

                {case['investigator']}

                <br/><br/>

                <b>Generated:</b><br/>

                {case['created_at']}

                <br/><br/><br/>

                Forensic Analysis of USB Device Usage on Windows Systems

                Using Automated Artifact Collection

                """,

                cover_text

            )

        )


        elements.append(

            PageBreak()

        )



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

            ["Artifact","Count"],

            ["USB Devices",len(devices)],

            ["Mounted Devices",len(mounted)],

            ["Timeline Events",len(timeline)],

            ["Correlations",len(correlations)]

        ])



        summary.setStyle(

            TableStyle([

                ("GRID",(0,0),(-1,-1),1,colors.black)

            ])

        )


        elements.append(summary)



        elements.append(PageBreak())



        # ==================================================
        # USB ARTIFACTS
        # ==================================================

        elements.append(

            Paragraph(

                "USB DEVICE ARTIFACTS",

                styles["Heading1"]

            )

        )



        for device in devices:


            table = Table([

                ["Manufacturer",device.manufacturer],

                ["Product",device.product],

                ["Revision",device.revision],

                ["Serial Number",device.serial_number],

                ["Registry Path",device.registry_path],

                ["Registry Time",device.registry_time],

                [

                    "SHA-256",

                    HashUtils.sha256(device.__dict__)

                ]

            ])


            table.setStyle(

                TableStyle([

                    ("GRID",(0,0),(-1,-1),1,colors.black)

                ])

            )


            elements.append(table)

            elements.append(

                Spacer(1,20)

            )



        # ==================================================
        # MOUNTED DEVICES
        # ==================================================

        elements.append(

            Paragraph(

                "MOUNTED DEVICE ARTIFACTS",

                styles["Heading1"]

            )

        )



        for mount in mounted:


            table = Table([

                ["Drive Letter",mount.drive_letter],

                ["Registry Name",mount.registry_name],

                ["Volume GUID",mount.volume_guid],

                ["Registry Time",mount.registry_time],

                [

                    "SHA-256",

                    HashUtils.sha256(mount.__dict__)

                ]

            ])



            table.setStyle(

                TableStyle([

                    ("GRID",(0,0),(-1,-1),1,colors.black)

                ])

            )


            elements.append(table)

            elements.append(

                Spacer(1,20)

            )



        elements.append(PageBreak())



        # ==================================================
        # FORENSIC TIMELINE
        # ==================================================

        elements.append(

            Paragraph(

                "FORENSIC TIMELINE",

                styles["Heading1"]

            )

        )



        timeline_data = [

            [

                "Time",

                "Artifact",

                "Description"

            ]

        ]



        for event in timeline:


            timeline_data.append([

                event["time"],

                event["artifact"],

                event["description"]

            ])



        timeline_table = Table(

            timeline_data

        )


        timeline_table.setStyle(

            TableStyle([

                ("GRID",(0,0),(-1,-1),1,colors.black)

            ])

        )


        elements.append(timeline_table)



        # ==================================================
        # CORRELATIONS
        # ==================================================

        elements.append(

            Paragraph(

                "CORRELATION ANALYSIS",

                styles["Heading1"]

            )

        )



        for item in correlations:


            elements.append(

                Paragraph(

                    f"""

                    <b>Device:</b> {item['product']}<br/>

                    <b>Drive:</b> {item['drive_letter']}<br/>

                    <b>Confidence:</b> {item['confidence']}%

                    """,

                    styles["Normal"]

                )

            )



            elements.append(

                Paragraph(

                    "Supporting Evidence:",

                    styles["Normal"]

                )

            )



            for key,value in item.get(

                "evidence",

                {}

            ).items():


                elements.append(

                    Paragraph(

                        f"{key}: {value}",

                        styles["Normal"]

                    )

                )



            elements.append(

                Spacer(1,15)

            )



        # ==================================================
        # CONCLUSION
        # ==================================================

        elements.append(PageBreak())


        elements.append(

            Paragraph(

                "FORENSIC CONCLUSION",

                styles["Heading1"]

            )

        )



        conclusion = """

        This investigation was performed using the USB Forensics Analyzer

        automated evidence collection framework.



        The system collected Windows USB-related artifacts from registry

        locations, mounted device records, and Windows Event Logs.



        Registry timestamps, mounted device timestamps, and event log

        timestamps were combined to reconstruct a chronological timeline

        of USB device activity.



        SHA-256 hashing was applied to collected artifacts to support

        evidence integrity verification.



        The findings represent the results of automated forensic artifact

        collection and correlation performed during this investigation.

        """



        elements.append(

            Paragraph(

                conclusion,

                styles["Normal"]

            )

        )



        document.build(

            elements,

            onFirstPage=PDFReport.add_footer,

            onLaterPages=PDFReport.add_footer

        )



        print(

            f"\n[+] PDF report generated: {PDFReport.OUTPUT_FILE}"

        )