from pathlib import Path
import os

from reportlab.lib.pagesizes import A4, landscape
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
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from utils.hash_utils import HashUtils
from utils.app_paths import AppPaths


AppPaths.initialize()



class PDFReport:


    OUTPUT_DIR = (

        Path(os.getenv("LOCALAPPDATA"))

        / "USBForensicsAnalyzer"

        / "output"

    )


    OUTPUT_FILE = OUTPUT_DIR / "case_report.pdf"



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

            760,

            25,

            f"Page {doc.page}"

        )


        canvas.restoreState()



    @staticmethod
    def create_styles():

        styles = getSampleStyleSheet()


        return {


            "title": ParagraphStyle(

                "CoverTitle",

                parent=styles["Title"],

                fontSize=22,

                alignment=TA_CENTER,

                spaceAfter=20

            ),



            "heading": ParagraphStyle(

                "Heading",

                parent=styles["Heading2"],

                fontSize=14,

                alignment=TA_LEFT,

                spaceBefore=12,

                spaceAfter=12

            ),



            "center": ParagraphStyle(

                "Center",

                parent=styles["Normal"],

                alignment=TA_CENTER

            ),



            "wrap": ParagraphStyle(

                "Wrap",

                parent=styles["Normal"],

                fontSize=7,

                leading=9,

                alignment=TA_LEFT

            ),



            "small": ParagraphStyle(

                "Small",

                parent=styles["Normal"],

                fontSize=9,

                leading=12

            )

        }



    @staticmethod
    def P(text, style):

        if text is None:

            text = ""


        return Paragraph(

            str(text),

            style

        )



    # ==================================================
    # SAFE DATA HANDLING
    # ==================================================


    @staticmethod
    def safe_value(data, key, default="UNKNOWN"):


        value = data.get(

            key,

            default

        )


        if value is None or value == "":

            return default


        return value



    # ==================================================
    # TIMELINE CLEANING
    # ==================================================


    @staticmethod
    def get_event_time(event):


        for key in [

            "time",

            "timestamp",

            "event_time",

            "created_at",

            "datetime"

        ]:


            if key in event and event[key]:

                return event[key]


        return "UNKNOWN"



    @staticmethod
    def get_event_label(event):

        """
        Converts raw Windows Event IDs
        into investigator friendly events.
        """


        event_id = event.get(

            "event_id",

            None

        )


        labels = {


            2003:

            "USB DEVICE CONNECTED",



            2001:

            "USB DEVICE INSTALLATION",



            2100:

            "USB DEVICE CONFIGURATION",



            2102:

            "USB DEVICE CONFIGURATION",



            1006:

            "DEVICE DRIVER ACTIVITY",



            1010:

            "DEVICE DRIVER ACTIVITY",



            400:

            "DEVICE STATE CHANGE",



            410:

            "DEVICE STATE CHANGE"

        }



        return labels.get(

            event_id,

            "USB ACTIVITY DETECTED"

        )



    @staticmethod
    def clean_timeline(timeline):

        """
        Removes duplicate noisy Windows
        event entries before reporting.
        """


        cleaned = []


        seen = set()



        for event in timeline:


            if hasattr(

                event,

                "to_dict"

            ):

                event = event.to_dict()



            label = PDFReport.get_event_label(

                event

            )


            key = (

                PDFReport.get_event_time(event),

                label,

                event.get(

                    "description",

                    ""

                )

            )



            if key in seen:

                continue



            seen.add(key)



            cleaned.append({

                "time":

                PDFReport.get_event_time(event),


                "artifact":

                label,


                "source":

                event.get(

                    "source",

                    "Windows Event Log"

                ),


                "description":

                event.get(

                    "description",

                    "USB activity detected"

                )

            })



        return cleaned



    @staticmethod
    def generate(

            case,

            devices,

            mounted,

            correlations,

            timeline):


        PDFReport.OUTPUT_DIR.mkdir(

            exist_ok=True

        )


        # Clean timeline before report generation

        timeline = PDFReport.clean_timeline(

            timeline

        )


        styles = PDFReport.create_styles()



        document = SimpleDocTemplate(

            str(PDFReport.OUTPUT_FILE),

            pagesize=landscape(A4),

            rightMargin=40,

            leftMargin=40,

            topMargin=40,

            bottomMargin=40

        )


        elements = []

                # ==================================================
        # COVER PAGE
        # ==================================================


        elements.append(

            Spacer(

                1,

                120

            )

        )


        elements.append(

            PDFReport.P(

                "USB FORENSICS ANALYZER",

                styles["title"]

            )

        )


        elements.append(

            PDFReport.P(

                "FORENSIC INVESTIGATION REPORT",

                styles["title"]

            )

        )


        elements.append(

            Spacer(

                1,

                50

            )

        )


        elements.append(

            PDFReport.P(

                f"""

                <b>Case ID:</b> {case.get("case_id","UNKNOWN")}

                <br/><br/>

                <b>Case Name:</b> {case.get("case_name","UNKNOWN")}

                <br/><br/>

                <b>Investigator:</b> {case.get("investigator","UNKNOWN")}

                <br/><br/>

                <b>Generated:</b> {case.get("created_at","UNKNOWN")}

                <br/><br/>

                Forensic Analysis of USB Device Usage

                on Windows Systems Using Automated Collection

                """,

                styles["center"]

            )

        )


        elements.append(

            PageBreak()

        )



        # ==================================================
        # CASE INFORMATION
        # ==================================================


        elements.append(

            PDFReport.P(

                "CASE INFORMATION",

                styles["heading"]

            )

        )



        case_table = Table(

            [

                [

                    "Case ID",

                    case.get(

                        "case_id",

                        "UNKNOWN"

                    )

                ],

                [

                    "Case Name",

                    case.get(

                        "case_name",

                        "UNKNOWN"

                    )

                ],

                [

                    "Investigator",

                    case.get(

                        "investigator",

                        "UNKNOWN"

                    )

                ],

                [

                    "Created",

                    case.get(

                        "created_at",

                        "UNKNOWN"

                    )

                ]

            ],

            colWidths=[

                120,

                300

            ]

        )


        case_table.setStyle(

            TableStyle([

                (

                    "GRID",

                    (0,0),

                    (-1,-1),

                    0.5,

                    colors.black

                )

            ])

        )


        elements.append(

            case_table

        )


        elements.append(

            Spacer(

                1,

                25

            )

        )



        summary_table = Table(

            [

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

                    "Timeline Activities",

                    len(timeline)

                ],

                [

                    "Correlation Findings",

                    len(correlations)

                ]

            ],

            colWidths=[

                200,

                100

            ]

        )



        summary_table.setStyle(

            TableStyle([

                (

                    "GRID",

                    (0,0),

                    (-1,-1),

                    0.5,

                    colors.black

                )

            ])

        )


        elements.append(

            summary_table

        )


        elements.append(

            PageBreak()

        )




        # ==================================================
        # USB DEVICE ARTIFACTS
        # ==================================================


        elements.append(

            PDFReport.P(

                "USB DEVICE ARTIFACTS",

                styles["heading"]

            )

        )



        usb_data = [

            [

                "Manufacturer",

                "Product",

                "Serial Number",

                "Registry Path",

                "Timestamp",

                "SHA256"

            ]

        ]



        for device in devices:


            device_hash = HashUtils.sha256(

                device.to_dict()

            )


            usb_data.append(

                [

                    PDFReport.P(

                        getattr(

                            device,

                            "manufacturer",

                            "UNKNOWN"

                        ),

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        getattr(

                            device,

                            "product",

                            "UNKNOWN"

                        ),

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        getattr(

                            device,

                            "serial_number",

                            "UNKNOWN"

                        ),

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        getattr(

                            device,

                            "registry_path",

                            "UNKNOWN"

                        ),

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        getattr(

                            device,

                            "registry_timestamp",

                            "UNKNOWN"

                        ),

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        device_hash,

                        styles["wrap"]

                    )

                ]

            )



        usb_table = Table(

            usb_data,

            repeatRows=1,

            colWidths=[

                80,

                80,

                120,

                190,

                90,

                130

            ]

        )


        usb_table.setStyle(

            TableStyle([

                (

                    "GRID",

                    (0,0),

                    (-1,-1),

                    0.5,

                    colors.black

                )

            ])

        )


        elements.append(

            usb_table

        )


        elements.append(

            PageBreak()

        )



        # ==================================================
        # MOUNTED DEVICE ARTIFACTS
        # ==================================================


        elements.append(

            PDFReport.P(

                "MOUNTED DEVICE ARTIFACTS",

                styles["heading"]

            )

        )


        mounted_data = [

            [

                "Drive",

                "Registry Name",

                "Volume GUID",

                "Timestamp",

                "SHA256"

            ]

        ]



        for mount in mounted:


            mounted_hash = HashUtils.sha256(

                mount.to_dict()

            )


            mounted_data.append(

                [

                    PDFReport.P(

                        getattr(

                            mount,

                            "drive_letter",

                            "UNKNOWN"

                        ),

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        getattr(

                            mount,

                            "registry_name",

                            "UNKNOWN"

                        ),

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        str(

                            getattr(

                                mount,

                                "volume_guid",

                                "UNKNOWN"

                            )

                        ),

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        getattr(

                            mount,

                            "registry_timestamp",

                            "UNKNOWN"

                        ),

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        mounted_hash,

                        styles["wrap"]

                    )

                ]

            )


        mounted_table = Table(

            mounted_data,

            repeatRows=1,

            colWidths=[

                80,

                200,

                130,

                100,

                150

            ]

        )


        mounted_table.setStyle(

            TableStyle([

                (

                    "GRID",

                    (0,0),

                    (-1,-1),

                    0.5,

                    colors.black

                )

            ])

        )


        elements.append(

            mounted_table

        )


        elements.append(

            PageBreak()

        )

                # ==================================================
        # FORENSIC TIMELINE
        # ==================================================


        elements.append(

            PDFReport.P(

                "FORENSIC TIMELINE",

                styles["heading"]

            )

        )



        timeline_data = [

            [

                "Time",

                "Activity",

                "Evidence Source",

                "Description"

            ]

        ]



        for event in timeline:



            timeline_data.append(

                [

                    PDFReport.P(

                        event.get(

                            "time",

                            "UNKNOWN"

                        ),

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        event.get(

                            "artifact",

                            "USB ACTIVITY"

                        ),

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        event.get(

                            "source",

                            "Windows Artifact"

                        ),

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        event.get(

                            "description",

                            "USB activity detected"

                        ),

                        styles["wrap"]

                    )

                ]

            )



        timeline_table = Table(

            timeline_data,

            repeatRows=1,

            colWidths=[

                120,

                150,

                150,

                300

            ]

        )



        timeline_table.setStyle(

            TableStyle([

                (

                    "GRID",

                    (0,0),

                    (-1,-1),

                    0.5,

                    colors.black

                )

            ])

        )


        elements.append(

            timeline_table

        )


        elements.append(

            PageBreak()

        )



               # ==================================================
        # CORRELATION ANALYSIS
        # ==================================================

        elements.append(

            PDFReport.P(

                "CORRELATION ANALYSIS",

                styles["heading"]

            )

        )



        correlation_data = [

            [

                "Manufacturer",

                "Product",

                "Serial Number",

                "Drive",

                "Volume GUID",

                "Container ID",

                "Friendly Name",

                "Confidence",

                "Reasons"

            ]

        ]



        for item in correlations:


            confidence = item.get(

                "confidence",

                0

            )


            confidence = f"{confidence}%"



            reasons = item.get(

                "reasons",

                []

            )


            if not reasons:

                reasons = [

                    "No correlation reason provided"

                ]



            correlation_data.append(

                [

                    PDFReport.P(

                        item.get(

                            "manufacturer",

                            "UNKNOWN"

                        ),

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        item.get(

                            "product",

                            "UNKNOWN"

                        ),

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        item.get(

                            "serial_number",

                            "UNKNOWN"

                        ),

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        item.get(

                            "drive_letter",

                            "UNKNOWN"

                        ),

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        item.get(

                            "volume_guid",

                            "UNKNOWN"

                        ),

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        item.get(

                            "container_id",

                            "UNKNOWN"

                        ),

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        item.get(

                            "friendly_name",

                            "UNKNOWN"

                        ),

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        confidence,

                        styles["wrap"]

                    ),


                    PDFReport.P(

                        ", ".join(

                            reasons

                        ),

                        styles["wrap"]

                    )

                ]

            )



        correlation_table = Table(

            correlation_data,

            repeatRows=1,

            colWidths=[

                65,   # Manufacturer

                70,   # Product

                100,  # Serial

                45,   # Drive

                100,  # Volume GUID

                90,   # Container ID

                100,  # Friendly Name

                55,   # Confidence

                160   # Reasons

            ]

        )



        correlation_table.setStyle(

            TableStyle([

                (

                    "GRID",

                    (0,0),

                    (-1,-1),

                    0.5,

                    colors.black

                )

            ])

        )



        elements.append(

            correlation_table

        )


        elements.append(

            PageBreak()

        )


        # ==================================================
        # FORENSIC CONCLUSION
        # ==================================================


        elements.append(

            PDFReport.P(

                "FORENSIC CONCLUSION",

                styles["heading"]

            )

        )


        conclusion = f"""

        This investigation collected and analyzed Windows USB artifacts.

        <br/><br/>

        <b>Collected Evidence Summary:</b>

        <br/>

        USB Devices Identified: {len(devices)}

        <br/>

        Mounted Devices Identified: {len(mounted)}

        <br/>

        Timeline Activities Reconstructed: {len(timeline)}

        <br/>

        Correlation Findings Generated: {len(correlations)}

        <br/><br/>

        Evidence integrity was preserved using SHA-256 hashing.

        Registry artifacts, mounted device mappings, and Windows

        activity records were analyzed to reconstruct USB device usage.

        <br/><br/>

        Raw Windows event identifiers are preserved internally

        for forensic validation while this report presents

        investigator-readable findings.

        <br/><br/>

        This report represents the automated forensic acquisition

        results generated by USB Forensics Analyzer.

        """



        elements.append(

            PDFReport.P(

                conclusion,

                styles["small"]

            )

        )



        # ==================================================
        # BUILD PDF
        # ==================================================


        document.build(

            elements,

            onFirstPage=PDFReport.add_footer,

            onLaterPages=PDFReport.add_footer

        )



        print(

            f"[+] PDF report generated: {PDFReport.OUTPUT_FILE}"

        )