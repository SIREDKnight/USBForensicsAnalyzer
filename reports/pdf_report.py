from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from pathlib import Path


class PDFReport:

    OUTPUT_FILE = Path("output") / "case_report.pdf"

    @staticmethod
    def generate(case, devices, mounted, correlations, timeline):

        doc = SimpleDocTemplate(str(PDFReport.OUTPUT_FILE), pagesize=A4)
        styles = getSampleStyleSheet()
        content = []

        # -------------------------
        # CASE INFO
        # -------------------------
        content.append(Paragraph("FORENSIC CASE REPORT", styles["Title"]))
        content.append(Spacer(1, 12))

        if case:
            content.append(Paragraph(f"Case ID: {case[0]}", styles["Normal"]))
            content.append(Paragraph(f"Case Name: {case[1]}", styles["Normal"]))
            content.append(Paragraph(f"Created At: {case[2]}", styles["Normal"]))
            content.append(Paragraph(f"Investigator: {case[3]}", styles["Normal"]))

        content.append(Spacer(1, 12))

        # -------------------------
        # DEVICES
        # -------------------------
        content.append(Paragraph("USB DEVICES", styles["Heading2"]))

        for d in devices:
            text = f"{d.manufacturer} | {d.product} | {d.serial_number}"
            content.append(Paragraph(text, styles["Normal"]))

        content.append(Spacer(1, 12))

        # -------------------------
        # MOUNTED
        # -------------------------
        content.append(Paragraph("MOUNTED DEVICES", styles["Heading2"]))

        for m in mounted:
            text = f"{m.drive_letter} | {m.registry_name}"
            content.append(Paragraph(text, styles["Normal"]))

        content.append(Spacer(1, 12))

        # -------------------------
        # CORRELATIONS
        # -------------------------
        content.append(Paragraph("CORRELATIONS", styles["Heading2"]))

        for c in correlations:
            text = f"{c['serial_number']} → {c['drive_letter']} ({c['confidence']}%)"
            content.append(Paragraph(text, styles["Normal"]))

        content.append(Spacer(1, 12))

        # -------------------------
        # TIMELINE
        # -------------------------
        content.append(Paragraph("TIMELINE", styles["Heading2"]))

        for t in timeline:
            text = f"{t[0]} | {t[1]} | {t[2]}"
            content.append(Paragraph(text, styles["Normal"]))

        # -------------------------
        # BUILD PDF
        # -------------------------
        doc.build(content)

        print(f"\n[+] PDF report generated: {PDFReport.OUTPUT_FILE}")