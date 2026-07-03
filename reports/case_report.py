import json
from pathlib import Path


class CaseReport:

    OUTPUT_DIR = Path("output")

    @staticmethod
    def generate(case, devices, mounted, correlations, timeline):

        report = {
            "case": {
                "id": case[0] if case else None,
                "name": case[1] if case else None,
                "created_at": case[2] if case else None,
                "investigator": case[3] if case else None,
            },
            "usb_devices": [],
            "mounted_devices": [],
            "correlations": correlations,
            "timeline": []
        }

        # USB DEVICES
        for d in devices:
            report["usb_devices"].append({
                "manufacturer": d.manufacturer,
                "product": d.product,
                "revision": d.revision,
                "serial_number": d.serial_number,
                "registry_path": d.registry_path
            })

        # MOUNTED DEVICES
        for m in mounted:
            report["mounted_devices"].append({
                "drive_letter": m.drive_letter,
                "registry_name": m.registry_name
            })

        # TIMELINE
        for t in timeline:
            report["timeline"].append({
                "event_time": t[0],
                "artifact": t[1],
                "description": t[2]
            })

        # CREATE OUTPUT FOLDER (FIX)
        CaseReport.OUTPUT_DIR.mkdir(exist_ok=True)

        output_file = CaseReport.OUTPUT_DIR / "case_report.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)

        print(f"\n[+] Forensic case report generated: {output_file}")