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
        # CUSTOM STYLES
        # ==================================================

        cover_title = ParagraphStyle(

            "CoverTitle",

            parent=styles["Title"],

            alignment=TA_CENTER,

            fontSize=24,

            spaceAfter=30

        )



        cover_text = ParagraphStyle(

            "CoverText",

            parent=styles["Normal"],

            alignment=TA_CENTER,

            fontSize=12,

            leading=18

        )



        # ==================================================
        # COVER PAGE
        # ==================================================

        elements.append(

            Spacer(

                1,

                100

            )

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

            Spacer(

                1,

                40

            )

        )



        case_id = case["case_id"]

        case_name = case["case_name"]

        investigator = case["investigator"]

        created = case["created_at"]



        cover_information = f"""

        <b>Case ID:</b><br/>

        {case_id}

        <br/><br/>

        <b>Case Name:</b><br/>

        {case_name}

        <br/><br/>

        <b>Investigator:</b><br/>

        {investigator}

        <br/><br/>

        <b>Generated:</b><br/>

        {created}

        <br/><br/><br/>

        <b>Forensic Analysis of USB Device Usage on Windows Systems

        Using Automated Artifact Collection</b>

        """



        elements.append(

            Paragraph(

                cover_information,

                cover_text

            )

        )



        elements.append(

            Spacer(

                1,

                100

            )

        )



        elements.append(

            Paragraph(

                "CONFIDENTIAL FORENSIC DOCUMENT",

                cover_text

            )

        )



        elements.append(

            PageBreak()

        )



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

            [

                "Case ID",

                case_id

            ],

            [

                "Case Name",

                case_name

            ],

            [

                "Investigator",

                investigator

            ],

            [

                "Created",

                created

            ]

        ])



        case_table.setStyle(

            TableStyle([

                (

                    "GRID",

                    (0,0),

                    (-1,-1),

                    1,

                    colors.black

                ),

                (

                    "BACKGROUND",

                    (0,0),

                    (0,-1),

                    colors.lightgrey

                )

            ])

        )



        elements.append(case_table)


        elements.append(

            Spacer(

                1,

                20

            )

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



        summary_table = Table([

            [

                "Artifact",

                "Count"

            ],

            [

                "USB Devices",

                len(devices)

            ],

            [

                "Mounted Devices",

                len(mounted)

            ],

            [

                "Timeline Events",

                len(timeline)

            ],

            [

                "Correlations",

                len(correlations)

            ]

        ])



        summary_table.setStyle(

            TableStyle([

                (

                    "GRID",

                    (0,0),

                    (-1,-1),

                    1,

                    colors.black

                )

            ])

        )



        elements.append(summary_table)



        elements.append(

            PageBreak()

        )



        # ==================================================
        # USB DEVICES
        # ==================================================

        elements.append(

            Paragraph(

                "USB DEVICE ARTIFACTS",

                styles["Heading1"]

            )

        )



        for device in devices:


            table = Table([

                [

                    "Manufacturer",

                    device.manufacturer

                ],

                [

                    "Product",

                    device.product

                ],

                [

                    "Revision",

                    device.revision

                ],

                [

                    "Serial Number",

                    device.serial_number

                ],

                [

                    "Registry Path",

                    device.registry_path

                ],

                [

                    "SHA-256",

                    HashUtils.sha256(

                        device.__dict__

                    )

                ]

            ])



            table.setStyle(

                TableStyle([

                    (

                        "GRID",

                        (0,0),

                        (-1,-1),

                        1,

                        colors.black

                    )

                ])

            )


            elements.append(table)

            elements.append(

                Spacer(

                    1,

                    15

                )

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

                [

                    "Drive Letter",

                    mount.drive_letter

                ],

                [

                    "Registry Name",

                    mount.registry_name

                ],

                [

                    "Volume GUID",

                    mount.volume_guid

                ],

                [

                    "SHA-256",

                    HashUtils.sha256(

                        mount.__dict__

                    )

                ]

            ])



            table.setStyle(

                TableStyle([

                    (

                        "GRID",

                        (0,0),

                        (-1,-1),

                        1,

                        colors.black

                    )

                ])

            )


            elements.append(table)



        # ==================================================
        # TIMELINE
        # ==================================================

        elements.append(

            PageBreak()

        )



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

                (

                    "GRID",

                    (0,0),

                    (-1,-1),

                    1,

                    colors.black

                )

            ])

        )



        elements.append(timeline_table)



        # ==================================================
        # CORRELATION
        # ==================================================

        elements.append(

            Spacer(

                1,

                20

            )

        )



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

                    Device: {item['product']}<br/>

                    Drive: {item['drive_letter']}<br/>

                    Confidence Score: {item['confidence']}%

                    """,

                    styles["Normal"]

                )

            )


            for reason in item["reasons"]:


                elements.append(

                    Paragraph(

                        f"- {reason}",

                        styles["Normal"]

                    )

                )


            elements.append(

                Spacer(

                    1,

                    10

                )

            )



        # ==================================================
        # CONCLUSION
        # ==================================================

        elements.append(

            PageBreak()

        )



        elements.append(

            Paragraph(

                "FORENSIC CONCLUSION",

                styles["Heading1"]

            )

        )



        conclusion = """

        This forensic investigation was conducted using the USB

        Forensics Analyzer automated evidence collection framework.



        The system collected and analyzed Windows USB-related

        artifacts including Registry information, mounted device

        records, and Windows Event Log entries.



        Collected artifacts were correlated to identify possible

        relationships between detected USB devices and mounted

        storage volumes.



        SHA-256 hashing was applied to collected evidence records

        to support integrity verification and demonstrate that

        evidence records can be validated after acquisition.



        The findings contained in this report represent the results

        of automated artifact collection and correlation performed

        during this investigation.

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