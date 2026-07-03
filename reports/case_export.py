import zipfile
from pathlib import Path


class CaseExport:

    OUTPUT_DIR = Path("output")

    @staticmethod
    def export(case_id):

        zip_path = CaseExport.OUTPUT_DIR / f"case_{case_id}_export.zip"

        # These are the files your system generates
        files = [
            CaseExport.OUTPUT_DIR / "case_report.pdf",
            CaseExport.OUTPUT_DIR / "usb_devices.json",
            Path("database") / "evidence.db"
        ]

        with zipfile.ZipFile(zip_path, "w") as zipf:

            for file in files:

                if file.exists():
                    zipf.write(file, arcname=file.name)

        print(f"\n[+] Case exported: {zip_path}")