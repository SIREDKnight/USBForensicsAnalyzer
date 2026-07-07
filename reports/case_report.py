from pathlib import Path
import json


class CaseReport:

    OUTPUT_FILE = Path("output") / "case_report.json"

    @staticmethod
    def generate(case, devices, mounted, correlations, timeline):

        report = {}

        # -------------------------
        # CASE INFO
        # -------------------------
        if case:
            report["case"] = {
                "id": case[0],
                "name": case[1],
                "created_at": case[2],
                "investigator": case[3]
            }
        else:
            report["case"] = None

        # -------------------------
        # USB DEVICES
        # -------------------------
        report["usb_devices"] = []

        for d in devices:

            report["usb_devices"].append({
                "manufacturer": d.manufacturer,
                "product": d.product,
                "revision": d.revision,
                "serial_number": d.serial_number,
                "registry_path": d.registry_path
            })

        # -------------------------
        # MOUNTED DEVICES
        # -------------------------
        report["mounted_devices"] = []

        for m in mounted:

            report["mounted_devices"].append({
                "drive_letter": m.drive_letter,
                "registry_name": m.registry_name
            })

        # -------------------------
        # TIMELINE (FIXED - DICT FORMAT)
        # -------------------------
        report["timeline"] = []

        for t in timeline:

            report["timeline"].append({
                "event_time": t.get("time", "UNKNOWN"),
                "artifact": t.get("artifact", "UNKNOWN"),
                "description": t.get("description", "UNKNOWN")
            })

        # -------------------------
        # CORRELATIONS
        # -------------------------
        report["correlations"] = []

        for c in correlations:

            report["correlations"].append({
                "device": c["device"].product,
                "serial_number": c["device"].serial_number,
                "drive_letter": c["drive_letter"],
                "score": c["score"],
                "reasons": c["reasons"]
            })

        # -------------------------
        # SAVE FILE
        # -------------------------
        with open(CaseReport.OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)

        print(f"\n[+] Case report generated: {CaseReport.OUTPUT_FILE}")