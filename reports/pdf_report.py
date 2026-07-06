from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from pathlib import Path


class PDFReport:

    OUTPUT_FILE = Path("output") / "case_report.pdf"

    @staticmethod
    def generate(case, devices, mounted, correlations, timeline):

        doc = SimpleDocTemplate(str(PDFReport.OUTPUT_FILE))
        styles = getSampleStyleSheet()
        elements = []

        # -------------------------
        # CASE INFO
        # -------------------------
        elements.append(Paragraph("USB FORENSICS CASE REPORT", styles["Title"]))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph(f"Case ID: {case[0]}", styles["Normal"]))
        elements.append(Paragraph(f"Case Name: {case[1]}", styles["Normal"]))
        elements.append(Paragraph(f"Created: {case[2]}", styles["Normal"]))
        elements.append(Paragraph(f"Investigator: {case[3]}", styles["Normal"]))

        elements.append(Spacer(1, 20))

        # -------------------------
        # USB DEVICES
        # -------------------------
        elements.append(Paragraph("USB DEVICES", styles["Heading2"]))

        for d in devices:

            elements.append(Paragraph(
                f"{d.manufacturer} | {d.product} | {d.serial_number}",
                styles["Normal"]
            ))

        elements.append(Spacer(1, 15))

        # -------------------------
        # MOUNTED DEVICES
        # -------------------------
        elements.append(Paragraph("MOUNTED DEVICES", styles["Heading2"]))

        for m in mounted:

            elements.append(Paragraph(
                f"{m.drive_letter} | {m.registry_name}",
                styles["Normal"]
            ))

        elements.append(Spacer(1, 15))

        # -------------------------
        # EVENT / TIMELINE
        # -------------------------
        elements.append(Paragraph("FORENSIC TIMELINE", styles["Heading2"]))

        for t in timeline:

            elements.append(Paragraph(
                f"{t['time']} | {t['artifact']} | {t['description']}",
                styles["Normal"]
            ))

        elements.append(Spacer(1, 15))

        # -------------------------
        # CORRELATIONS
        # -------------------------
        elements.append(Paragraph("CORRELATION FINDINGS", styles["Heading2"]))

        for c in correlations:

            elements.append(Paragraph(
                f"Device: {c['device'].product}",
                styles["Normal"]
            ))

            elements.append(Paragraph(
                f"Drive: {c['drive_letter']} | Score: {c['score']}%",
                styles["Normal"]
            ))

            for r in c["reasons"]:
                elements.append(Paragraph(f"- {r}", styles["Normal"]))

            elements.append(Spacer(1, 10))

        # -------------------------
        # CONCLUSION
        # -------------------------
        elements.append(Paragraph("CONCLUSION", styles["Heading2"]))

        elements.append(Paragraph(
            "This report summarizes USB device activity, "
            "mounted drive mapping, event logs, and correlation analysis.",
            styles["Normal"]
        ))

        doc.build(elements)

        print(f"\n[+] PDF report generated: {PDFReport.OUTPUT_FILE}")